#!/usr/bin/env python3
import logging
import subprocess
import platform
import argparse
import sys
import os
import glob
from bazecore_parser import ParseBazeCoreJSON
from get_serial import get_serial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from serial_plug import SerialPlug
import mainwindow

MAGNET_THRESHOLD = 45

TAB_DEFS = { 
    "light_tab":          {"conn": "fw", "avail": ['master','chinese'] },
    "function_tab":       {"conn": "fw", "avail": ['master','chinese'] },
    "magnet_tab":         {"conn": "fw", "avail": ['master','chinese'] },
    "load_defaults_tab":  {"conn": "fw", "avail": ['master','dvt','chinese'] },
    "neuron_firmware_tab":{"conn": "bl", "avail": ['master','dvt','chinese'] },
    }

left_keys       = 33 # 32 for ANSI
right_keys      = 36
left_led        = 30
right_led       = 32
led_start       = left_keys + right_keys
huble_leds      = 1
led_count       = left_keys + right_keys + left_led + right_led + huble_leds # 130 + 1 for the huble

class QTLogHandler(logging.StreamHandler):

    def __init__(self, qt_app):
        logging.StreamHandler.__init__(self)
        self.qt_app = qt_app

    def emit(self, record):
        msg = self.format(record)
        self.qt_app.add_log(msg)

class CombinedTests(QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self, wd):
        super(self.__class__, self).__init__()

    def setup(self):
        self.clipboard = QApplication.clipboard()
        self.setupUi(self) 

        self.ser = SerialPlug()
        self.wd = wd

        # serial
        self.button_fetch_serial.clicked.connect(lambda: get_serial()) 
        # self.button_fetch_serial.clicked.connect(lambda: self.start_debug()) 
        reg_ex = QRegExp("^[0-9]N[0-9]{5}")
        self.serial_validator = QRegExpValidator(reg_ex, self.lineEdit_serial)
        self.lineEdit_serial.setValidator(self.serial_validator)

        self.light_red.clicked.connect(lambda: self.run_serial_cmd("led.setAll 255 0 0"))
        self.light_green.clicked.connect(lambda: self.run_serial_cmd("led.setAll 0 255 0"))
        self.light_blue.clicked.connect(lambda: self.run_serial_cmd("led.setAll 0 0 255"))
        self.light_white.clicked.connect(lambda: self.run_serial_cmd("led.setAll 255 255 255"))
        self.light_off.clicked.connect(lambda: self.run_serial_cmd("led.setAll 0 0 0"))

        # function mode
        self.button_switch_test.clicked.connect(lambda: self.run_serial_cmd("led.mode 3"))

        # magnet buttons
        self.magnet_split.clicked.connect(self.get_split_clicked)
        self.magnet_joined.clicked.connect(self.get_joined_clicked)
        self.magnet_restart.clicked.connect(self.magnet_restart_clicked)

        # load defaults
        self.load_defaults.clicked.connect(lambda: self.default_settings_clicked())

        # tab connections
        self.tabWidget.tabBarClicked.connect(self.tab_changed) # tabBarClicked only triggered on an actual click unlike currentChanged which gets triggered when a tab is updated in SW
        self.tabWidget.setCurrentIndex(0)

        # log copy menu
        self.actionCopy_log.triggered.connect(lambda: self.copy_log())
        self.actionClear_log.triggered.connect(lambda: self.clear_log())

        # neuron fw
        self.update_firmware.clicked.connect(lambda: self.bossa_update_firmware_clicked())
        try:
            self.firmware_file = glob.glob("*.bin")[0]
            self.label_firmware_file.setText(os.path.basename(self.firmware_file))
        except IndexError as e:
            logging.warning("couldn't find a default firmware")
            self.firmware_file = None

        # defaults file
        try:
            self.defaults_file = glob.glob("*.json")[0]
            self.label_defaults_file.setText(os.path.basename(self.defaults_file))
            self.defaults = ParseBazeCoreJSON(self.defaults_file).parse_all()
            self.load_defaults.setEnabled(True) 
        except IndexError as e:
            logging.warning("couldn't find defaults file")
            self.defaults_file = None
            self.load_defaults.setEnabled(False) 

        # remove tabs not available from command options
        for tab_name, tab_config in TAB_DEFS.items():
            if not args.gui_version in tab_config['avail']:
                tab = self.findChild(QWidget, tab_name)
                index = self.tabWidget.indexOf(tab)
                logging.debug("removing tab %d [%s]" % (index, tab_name))
                self.tabWidget.removeTab(index)

        # status bar timer that also does serial connection
        self.status_timer = QTimer(self)
        self.last_serial_check = None
        self.status_timer.timeout.connect(self.check_serial_status)
        self.status_timer.start(1000)
        self.check_serial_status()

        # start off with info tab
        self.select_led_tab()

        self.show()

    # serial command utilities
    ################################################################################

    @pyqtSlot()
    def run_serial_cmd(self, command):
        return self.ser.run_cmd(command)

    @pyqtSlot()
    def run_focus_cmd(self):
        self.run_serial_cmd(self.focus_cmd.text())
        self.focus_cmd.clear()

    # log utilities
    ################################################################################

    def copy_log(self):
        logging.debug("copy log")
        self.clipboard.clear(mode=self.clipboard.Clipboard )
        self.clipboard.setText(self.log_messages.toPlainText(), mode=self.clipboard.Clipboard)

    def clear_log(self):
        logging.debug("clear log")
        self.log_messages.clear()

    def add_log(self, msg):
        self.log_messages.appendPlainText(msg)

    # firmware
    ################################################################################

    def select_led_tab(self):
        # select another info tab - in all GUI versions
        tab = self.findChild(QWidget, "light_tab")
        index = self.tabWidget.indexOf(tab)
        self.tabWidget.setCurrentIndex(index)
        self.tab_changed(self.tabWidget.currentIndex())

    def bossa_update_firmware_clicked(self):
        logging.info("starting BOSSA firmware update with file %s" % self.firmware_file)
        if platform.system() == 'Linux':
            bossac = os.path.join(self.wd, 'binaries', 'bossac')
            command_list = [bossac, '-i', '-d', '--port', self.ser.get_port(), '-e', '-o', '0x2000', '-w', self.firmware_file, '-R']
        elif platform.system() == 'Windows':
            bossac = os.path.join(self.wd, 'binaries', 'bossac.exe')
            # arduino compliled version of bossac already writes to offset 0x2000
            command_list = [bossac, '-i', '-d', '--port', self.ser.get_port(), '-e', '-w', self.firmware_file, '-R']
        else:
            # don't have anything for Mac
            logging.warning("unsupported platform %s" % platform.system())
            return

        logging.info(" ".join(command_list))
        result = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logging.info(result.stdout.decode('utf-8'))

    # defaults
    ################################################################################

    def default_settings_clicked(self):
        logging.info("loading the defaults")
        for default in self.defaults:
            logging.info(default)
            self.ser.run_cmd(default)

    # led tools
    ################################################################################

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

    # magnet
    ################################################################################

    # this gets called first
    @pyqtSlot()
    def get_joined_clicked(self):
        joined = int(self.ser.run_cmd("hardware.joint"))
        logging.info("joined = %d" % joined)
        if joined > 0 and joined < 1000:
            self.joined = joined
            self.magnet_joined.setDisabled(True)
            self.magnet_split.setEnabled(True)
        else:
            logging.warning("invalid joint value - is side plugged in?")
            self.magnet_fail.setStyleSheet("background-color: red")

    # and this after
    @pyqtSlot()
    def get_split_clicked(self):
        self.split = int(self.ser.run_cmd("hardware.joint"))
        logging.info("split = %d" % self.split)
        self.magnet_split.setDisabled(True)
        # joined is more than split
        self.threshold = (self.joined - self.split) / 2 + self.split;
        logging.info("new threshold = %d" % self.threshold)
        self.ser.run_cmd("joint.threshold %d" % self.threshold)

        if (self.joined - self.split) > MAGNET_THRESHOLD:
            self.magnet_pass.setStyleSheet("background-color: green")
        else:
            self.magnet_fail.setStyleSheet("background-color: red")
            logging.warning("magnet difference was %d, needs to be > %d" % (self.joined - self.split, MAGNET_THRESHOLD))

    @pyqtSlot()
    def magnet_restart_clicked(self):
        self.magnet_pass.setStyleSheet("background-color: grey")
        self.magnet_fail.setStyleSheet("background-color: grey")
        self.magnet_split.setDisabled(True)
        self.magnet_joined.setEnabled(True)

    # tab change stuff
    ################################################################################

    # called when a tab is clicked
    def tab_changed(self, index):
        try:
            tab_name = self.tabWidget.widget(index).objectName()
        except AttributeError:
            # can happen if clicked on disabled tab
            return
        
        self.clear_log()
        logging.debug("tab change to %s" % tab_name)
        if tab_name == "light_tab":
            self.ser.run_cmd("led.mode 8") # palette effect
            self.ser.run_cmd("led.setAll 0 0 0")
        elif tab_name == "magnet_tab":
            self.ser.run_cmd("led.mode 6") # joint effect mode
            self.magnet_restart_clicked()
        elif tab_name == "led_tab":
            self.ser.run_cmd("led.mode 8") # joint effect mode
            self.ser.run_cmd("led.setAll 0 0 0")
            self.next_led(0)
        elif tab_name == "info_tab":
            self.version_label.setText(self.run_serial_cmd("hardware.firmware"))
            self.keyscan_label.setText(self.run_serial_cmd("hardware.keyscan"))
            self.layout_label.setText(self.run_serial_cmd("hardware.layout"))

        # connection mode depends on the tab
        if TAB_DEFS[tab_name]["conn"] == 'fw':
            self.ser.find_keyboard()
        elif TAB_DEFS[tab_name]["conn"] == 'bl':
            self.ser.find_bootloader()

    # called regularly by the timer
    def check_serial_status(self):
        self.ser.check_serial_status()
        self.statusBar.showMessage(self.ser.get_status_message())

        # disable the tabs if no serial - except the neuron firmware one
        if not self.ser.is_connected():
            # have to record which tab was selected
            current_index = self.tabWidget.currentIndex()
            for index in range(self.tabWidget.count()):
                tab_name = self.tabWidget.widget(index).objectName()
                if not tab_name == "neuron_firmware_tab":
                    self.tabWidget.setTabEnabled(index, False)
            # so it can be reinstated
            self.tabWidget.setCurrentIndex(current_index)

        # if has just come back on line
        if self.ser.is_connected() and not self.last_serial_check:
            for index in range(self.tabWidget.count()):
                self.tabWidget.setTabEnabled(index, True)

            # get the keyboard ready for the test
            self.tab_changed(self.tabWidget.currentIndex())

        tab_name = self.tabWidget.currentWidget().objectName()

        # only allow firmware update button enabled if connected to bootloader
        if tab_name == "neuron_firmware_tab":
            if self.ser.is_connected() and self.firmware_file is not None and self.lineEdit_serial.hasAcceptableInput():
                self.update_firmware.setEnabled(True) 
            else:
                self.update_firmware.setEnabled(False) 

        # update the magnet level if on the magnet page
        if tab_name == "magnet_tab" and self.ser.is_connected():
            self.magnet_level.setValue(int(self.ser.run_cmd("hardware.joint", quiet=True)))

        self.last_serial_check = self.ser.is_connected()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Dygma Raise test jig controller")
    parser.add_argument('--verbose', '-v', help="use multiple times for more verbosity", action='count', default=1)
    parser.add_argument('--gui-version', help="switch between master, Chinese and DVT", action='store', default="master", choices=['master','chinese','dvt'])
    args = parser.parse_args()

    # working directory
    try:
       wd = sys._MEIPASS # if running inside pyinstaller
    except AttributeError:
       wd = os.getcwd()


    translator = QTranslator()
    if args.gui_version == 'chinese':
        file_path = os.path.join(wd, 'languages', 'china.qm')
        translator.load(file_path)

    app = QApplication(sys.argv)
    app.installTranslator(translator)
    form = CombinedTests(wd)

    """ 
    CRITICAL 50
    ERROR 40
    WARNING 30
    INFO 20
    DEBUG 10
    NOTSET 0
    """
    args.verbose = 40 - (10*args.verbose) if args.verbose > 0 else 0

    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)10s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(args.verbose)
    log.addHandler(ch)

    qtlog = QTLogHandler(form)
    qtlog.setLevel(logging.INFO)
    log.addHandler(qtlog)

    form.setup()

    # allow override gui with specific arguments
    ret = app.exec_()
    logging.info("finished")
    sys.exit(ret)
