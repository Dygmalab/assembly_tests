import logging
import mainwindow
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from serial_plug import SerialPlug

TABS = ["light", "magnet"]

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
        self.setupUi(self) # gets defined in the UI file

        self.ser = SerialPlug()

        self.light_red.clicked.connect(lambda: self.on_click("255 0 0"))
        self.light_green.clicked.connect(lambda: self.on_click("0 255 0"))
        self.light_blue.clicked.connect(lambda: self.on_click("0 0 255"))
        self.light_white.clicked.connect(lambda: self.on_click("255 255 255"))

        self.magnet_split.clicked.connect(self.get_split)
        self.magnet_joined.clicked.connect(self.get_joined)

        self.tabWidget.currentChanged.connect(self.tabChange)

        timer = QTimer(self)
        timer.timeout.connect(self.checkSerialStatus)
        timer.start(1000)
        self.checkSerialStatus()

        self.tabChange(self.tabWidget.currentIndex())

        self.show()

    def tabChange(self, index):
        if not self.ser.is_connected():
            # ignore tab change because it was triggered by the disabling of the tab in checkSerialStatus()
            return
        logging.info("tab change to %s" % TABS[index])
        if TABS[index] == "light":
            self.ser.run_cmd("led.mode 8") # palette effect
            self.ser.run_cmd("led.setAll 0 0 0")
        elif TABS[index] == "magnet":
            self.ser.run_cmd("led.mode 6") # joint effect mode
            self.split = 300
            self.joined = 600
            self.update_thresh()
            pass

    # magnet stuff
    def update_thresh(self):
        if(self.split > self.joined):
            self.threshold = (self.split - self.joined) / 2 + self.joined;
        else:
            self.threshold = (self.joined - self.split) / 2 + self.split;
        logging.info("new threshold = %d" % self.threshold)
        self.ser.run_cmd("joint.threshold %d" % self.threshold)

    @pyqtSlot()
    def get_split(self):
        self.split = int(self.ser.run_cmd("hardware.joint"))
        logging.info("split = %d" % self.split)
        self.update_thresh()

    @pyqtSlot()
    def get_joined(self):
        self.joined = int(self.ser.run_cmd("hardware.joint"))
        logging.info("joined = %d" % self.joined)
        self.update_thresh()

    def checkSerialStatus(self):
        self.ser.check_serial_status()
        self.statusBar.showMessage(self.ser.get_status_message())
        for index, tab_name in enumerate(TABS):
            self.tabWidget.setTabEnabled(index, self.ser.is_connected());

    @pyqtSlot()
    def on_click(self, color_string):
        self.ser.run_cmd("led.setAll %s" % color_string)

    def add_log(self, msg):
        self.log_messages.appendPlainText(msg)


if __name__ == '__main__':
    # get logging started
    log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)

    # create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter for console
    ch.setFormatter(log_format)
    log.addHandler(ch)

    app = QApplication(sys.argv)
    form = CombinedTests()

    qtlog = QTLogHandler(form)
    qtlog.setLevel(logging.INFO)
    log.addHandler(qtlog)

    ret = app.exec_()
    logging.info("finished")
    sys.exit(ret)
