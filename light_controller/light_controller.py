import serial, time
import serial.tools.list_ports
import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
RAISE_VIDPID = '1209:2201'

class SerialPlug():

    def setup(self):
        ports = serial.tools.list_ports.grep(RAISE_VIDPID)
        for port in ports:
            try:
                logging.info("found %s port on %s" % (port.usb_description(), port.device))
                self.ser = serial.Serial (port.device, 9600, timeout = 2, write_timeout = 1)
                time.sleep(0.5) # let it settle
                return True
            except serial.serialutil.SerialException:
                return False

#    # communicate over serial
#    def run_cmd(self, cmd):
#        output = ""
#        logging.info(cmd)
#
#        try:
#            self.ser.write (cmd + "\n") # must write \n with no delay or 10% chance not receive command correctly!
#        except serial.writeTimeoutError:
#            logging.warning("write timeout")
#            return output
#
#        while True:
#            resultLine = self.ser.readline()
#
#            if resultLine == "\r\n" or resultLine == "\n":
#                resultLine = " "
#            else:
#                resultLine = resultLine.rstrip()
#
#            if resultLine == "." or resultLine == "":
#                break
#
#            if resultLine:
#                output += resultLine
#
#        logging.info(output)
#        return output

    def run_cmd(self, cmd):

        output = ""
        logging.info(cmd)
        try:
            self.ser.write (str.encode(cmd + "\n")) # must write \n with no delay or 10% chance not receive command correctly!
        except serial.writeTimeoutError:
            logging.warning("write timeout")
            return output

        while True:
            resultLine = self.ser.readline().decode('utf-8')

            if resultLine == "\r\n" or resultLine == "\n":
                resultLine = " "
            else:
                resultLine = resultLine.rstrip ()

            if resultLine == ".":
                break

            if resultLine:
                output += resultLine

        logging.info(output)
        return output

class App(QWidget):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.title = 'light controller demo'

        self.ser = SerialPlug()
        self.ser.setup()
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
