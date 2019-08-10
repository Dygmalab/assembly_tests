import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from serial_plug import SerialPlug


class App(QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.title = 'magnet calibrator'

        self.ser = SerialPlug()
        self.ser.run_cmd("led.mode 6") # joint effect mode

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
       
        self.split = int(self.ser.run_cmd("joint.split"))
        self.joined = int(self.ser.run_cmd("joint.joined"))
        self.update_thresh()

        button = QPushButton('keyboard split', self)
        button.move(100,50)
        button.clicked.connect(self.get_split)

        button = QPushButton('keyboard joined', self)
        button.move(100,50+40)
        button.clicked.connect(self.get_joined)

        self.show()

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
    # without this, the script exits immediately.
    ex = App()
    sys.exit(app.exec_())
