import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from serial_plug import SerialPlug


class App(QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.title = 'light controller demo'

        self.ser = SerialPlug()
        self.ser.run_cmd("led.mode 8") # palette effect
        self.ser.run_cmd("led.setAll 0 0 0")

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('red', self)
        button.move(100,50)
        button.clicked.connect(lambda: self.on_click("255 0 0"))

        button = QPushButton('green', self)
        button.move(100,50+40)
        button.clicked.connect(lambda: self.on_click("0 255 0"))

        button = QPushButton('blue', self)
        button.move(100,50+40+40)
        button.clicked.connect(lambda: self.on_click("0 0 255"))

        button = QPushButton('white', self)
        button.move(100,50+40+40+40)
        button.clicked.connect(lambda: self.on_click("255 255 255"))
        
        self.show()

    @pyqtSlot()
    def on_click(self, color_string):
        self.ser.run_cmd("led.setAll %s" % color_string)


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
