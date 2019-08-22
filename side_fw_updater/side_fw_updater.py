import logging
import mainwindow
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from serial_plug import SerialPlug

TABS = ["sidefw" ]

class QTLogHandler(logging.StreamHandler):

    def __init__(self, qt_app):
        logging.StreamHandler.__init__(self)
        self.qt_app = qt_app

    def emit(self, record):
        msg = self.format(record)
        self.qt_app.add_log(msg)

class SideFirmwareFlasher(QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()

    def setup(self):
        self.setupUi(self) # gets defined in the UI file
        self.clipboard = QApplication.clipboard()

        self.ser = SerialPlug()

        self.verify_left.clicked.connect(lambda: self.on_click("hardware.verify_left_side"))
        self.verify_right.clicked.connect(lambda: self.on_click("hardware.verify_right_side"))
        self.flash_left.clicked.connect(lambda: self.on_click("hardware.flash_left_side"))
        self.flash_right.clicked.connect(lambda: self.on_click("hardware.flash_right_side"))

        self.actionCopy_log.triggered.connect(lambda: self.copy_log())
        self.actionClear_log.triggered.connect(lambda: self.clear_log())

        self.tabWidget.currentChanged.connect(self.tabChange)
        self.tabWidget.setCurrentIndex(TABS.index("sidefw"))

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

    def tabChange(self, index):
        if not self.ser.is_connected():
            # ignore tab change because it was triggered by the disabling of the tab in checkSerialStatus()
            return
        logging.debug("tab change to %s" % TABS[index])
        if TABS[index] == "sidefw":
            pass

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

    @pyqtSlot()
    def on_click(self, command):
        self.ser.run_cmd(command)

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
    form = SideFirmwareFlasher()

    qtlog = QTLogHandler(form)
    qtlog.setLevel(logging.INFO)
    log.addHandler(qtlog)

    form.setup()

    ret = app.exec_()
    logging.info("finished")
    sys.exit(ret)
