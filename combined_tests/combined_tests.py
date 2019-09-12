import logging
import argparse
import mainwindow
import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from serial_plug import SerialPlug

TABS = ["light", "led", "magnet", "load defaults", "sidefw", "focus", "info" ]

left_keys        = 33 # 32 for ANSI
right_keys       = 36
left_led   = 30
right_led  = 32
led_start  = left_keys + right_keys
huble_leds       = 1
led_count = left_keys + right_keys + left_led + right_led + huble_leds # 130 + 1 for the huble

class QTLogHandler(logging.StreamHandler):

    def __init__(self, qt_app):
        logging.StreamHandler.__init__(self)
        self.qt_app = qt_app

    def emit(self, record):
        msg = self.format(record)
        self.qt_app.add_log(msg)

class CombinedTests(QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()

    def setup(self):
        self.setupUi(self) # gets defined in the UI file
        self.clipboard = QApplication.clipboard()

        self.ser = SerialPlug()


        # led tab buttons
        self.light_red.clicked.connect(lambda: self.run_serial_cmd("led.setAll 255 0 0"))
        self.light_green.clicked.connect(lambda: self.run_serial_cmd("led.setAll 0 255 0"))
        self.light_blue.clicked.connect(lambda: self.run_serial_cmd("led.setAll 0 0 255"))
        self.light_white.clicked.connect(lambda: self.run_serial_cmd("led.setAll 255 255 255"))
        self.light_off.clicked.connect(lambda: self.run_serial_cmd("led.setAll 0 0 0"))

        # magnet buttons
        self.magnet_split.clicked.connect(self.get_split)
        self.magnet_joined.clicked.connect(self.get_joined)

        # individual led buttons and setup
        self.current_led = 0
        self.last_led = None
        self.led_num.display(self.current_led)
        self.led_next.clicked.connect(lambda: self.next_led(+1))
        self.led_prev.clicked.connect(lambda: self.next_led(-1))

        # load defaults
        self.load_defaults.clicked.connect(lambda: self.defaults())

        # side fw updater
        self.verify_left.clicked.connect(lambda: self.run_serial_cmd("hardware.verify_left_side"))
        self.verify_right.clicked.connect(lambda: self.run_serial_cmd("hardware.verify_right_side"))
        self.flash_left.clicked.connect(lambda: self.run_serial_cmd("hardware.flash_left_side"))
        self.flash_right.clicked.connect(lambda: self.run_serial_cmd("hardware.flash_right_side"))

        # focus cmds
        self.focus_cmd.returnPressed.connect(lambda: self.run_focus_cmd())

        # tab connections
        self.tabWidget.currentChanged.connect(self.tabChange)
        self.tabWidget.setCurrentIndex(TABS.index("light"))

        # log copy menu
        self.actionCopy_log.triggered.connect(lambda: self.copy_log())
        self.actionClear_log.triggered.connect(lambda: self.clear_log())

        # status bar timer that also does serial connection
        timer = QTimer(self)
        self.last_serial_check = None
        timer.timeout.connect(self.checkSerialStatus)
        timer.start(1000)
        self.checkSerialStatus()

        self.show()

    def copy_log(self):
        logging.debug("copy log")
        self.clipboard.clear(mode=self.clipboard.Clipboard )
        self.clipboard.setText(self.log_messages.toPlainText(), mode=self.clipboard.Clipboard)

    def clear_log(self):
        logging.debug("clear log")
        self.log_messages.clear()
    
    def defaults(self):
        settings = ["keymap.custom", "colormap.map", "palette", "keymap.onlyCustom", "hardware.keyscan", 
                    "idleLeds.idleTimeLimit", "led.mode"]
        try:
           wd = sys._MEIPASS # if running inside pyinstaller
        except AttributeError:
           wd = os.getcwd()

        for conf in settings:
            file_path = os.path.join(wd, 'defaults', "DVT" + conf)
            with open(file_path, 'r') as fh:
                data = fh.readline()
                data = data.strip()
                self.ser.run_cmd("%s %s" % (conf, data))

    def next_led(self, increment):
        self.current_led += increment

        if self.current_led >= led_count:
            self.current_led = 0
        if self.current_led < 0:
            self.current_led = led_count - 1

        self.led_num.display(self.current_led)
        self.ser.run_cmd("led.at %d 255 255 255" % self.current_led)

        if self.last_led is not None:
            self.ser.run_cmd("led.at %d 0 0 0" % self.last_led)

        self.last_led = self.current_led

    def tabChange(self, index):
        if not self.ser.is_connected():
            # ignore tab change because it was triggered by the disabling of the tab in checkSerialStatus()
            return
        logging.debug("tab change to %s" % TABS[index])
        if TABS[index] == "light":
            self.ser.run_cmd("led.mode 8") # palette effect
            self.ser.run_cmd("led.setAll 0 0 0")
        elif TABS[index] == "magnet":
            self.ser.run_cmd("led.mode 6") # joint effect mode
            self.magnet_split.setDisabled(True)
            self.magnet_joined.setEnabled(True)
        elif TABS[index] == "led":
            self.ser.run_cmd("led.mode 8") # joint effect mode
            self.ser.run_cmd("led.setAll 0 0 0")
            self.next_led(0)
        elif TABS[index] == "info":
            self.version_label.setText(self.run_serial_cmd("hardware.firmware"))
            self.keyscan_label.setText(self.run_serial_cmd("hardware.keyscan"))
            self.layout_label.setText(self.run_serial_cmd("hardware.layout"))

    # magnet stuff
    # this gets called first
    @pyqtSlot()
    def get_joined(self):
        joined = int(self.ser.run_cmd("hardware.joint"))
        logging.info("joined = %d" % joined)
        if joined > 0 and joined < 1000:
            self.joined = joined
            self.magnet_joined.setDisabled(True)
            self.magnet_split.setEnabled(True)
        else:
            logging.warning("invalid joint value - is side plugged in?")

    # and this after
    @pyqtSlot()
    def get_split(self):
        self.split = int(self.ser.run_cmd("hardware.joint"))
        logging.info("split = %d" % self.split)
        self.magnet_split.setDisabled(True)
        if(self.split > self.joined):
            self.threshold = (self.split - self.joined) / 2 + self.joined;
        else:
            self.threshold = (self.joined - self.split) / 2 + self.split;
        logging.info("new threshold = %d" % self.threshold)
        self.ser.run_cmd("joint.threshold %d" % self.threshold)

    def checkSerialStatus(self):
        self.ser.check_serial_status()
        self.statusBar.showMessage(self.ser.get_status_message())

        # disable the tabs if no serial
        if not self.ser.is_connected():
            current_index = self.tabWidget.currentIndex()
            for index, tab_name in enumerate(TABS):
                self.tabWidget.setTabEnabled(index, False)
            self.tabWidget.setCurrentIndex(current_index)

        # if has just come back on line
        if self.ser.is_connected() and not self.last_serial_check:
            for index, tab_name in enumerate(TABS):
                self.tabWidget.setTabEnabled(index, True)

            # get the keyboard ready for the test
            self.tabChange(self.tabWidget.currentIndex())

        self.last_serial_check = self.ser.is_connected()

        # update the magnet level if on the magnet page
        if TABS[self.tabWidget.currentIndex()] == "magnet":
            self.magnet_level.setValue(int(self.ser.run_cmd("hardware.joint", quiet=True)))

    @pyqtSlot()
    def run_serial_cmd(self, command):
        return self.ser.run_cmd(command)

    @pyqtSlot()
    def run_focus_cmd(self):
        self.run_serial_cmd(self.focus_cmd.text())
        self.focus_cmd.clear()

    def add_log(self, msg):
        self.log_messages.appendPlainText(msg)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Dygma Raise test jig controller")
    parser.add_argument('--verbose', '-v', action='count', default=1)
    parser.add_argument('--chinese', action='store_const', const=True) # doesn't do anything yet
    parser.add_argument('--defaults', action='store_const', const=True)
    args = parser.parse_args()

    args.verbose = 70 - (10*args.verbose) if args.verbose > 0 else 0
    logging.basicConfig(level=args.verbose, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # get logging started
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)

    # create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    log.addHandler(ch)

    app = QApplication(sys.argv)
    form = CombinedTests()

    qtlog = QTLogHandler(form)
    qtlog.setLevel(logging.INFO)
    log.addHandler(qtlog)

    form.setup()

    # allow override gui with specific arguments
    if args.defaults:
        form.defaults()
    else:
        ret = app.exec_()
        logging.info("finished")
        sys.exit(ret)
