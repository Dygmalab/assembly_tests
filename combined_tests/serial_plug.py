import logging
import serial, time
import serial.tools.list_ports
RAISE_FW_VIDPID = '1209:2201'
RAISE_BL_VIDPID = '1209:2200'

class SerialPlug():

    def __init__(self):
        self.vidpid = RAISE_FW_VIDPID
        self.connected = False
        self.find_keyboard()
        self.ser = None

    def find_bootloader(self):
        if self.vidpid != RAISE_BL_VIDPID:
            self.connected = False
        self.vidpid = RAISE_BL_VIDPID

    def find_keyboard(self):
        if self.vidpid != RAISE_FW_VIDPID:
            self.connected = False
        self.vidpid = RAISE_FW_VIDPID

    def is_connected(self):
        return self.connected

    def get_status_message(self):
        if self.connected:
            if self.vidpid == RAISE_FW_VIDPID:
                return "connected to Raise on port %s" % self.port
            if self.vidpid == RAISE_BL_VIDPID:
                return "connected to bootloader on port %s" % self.port
        else:
            return("trying to connect to a Raise...")

    def check_serial_status(self):
        if self.connected:
            # try a write if connected to FW
            if self.vidpid == RAISE_FW_VIDPID:
                logging.debug("trying a write to check serial")
                self.run_cmd("", quiet=True)
            # nothing if bootloader
        else:
            # otherwise try to setup
            logging.debug("calling setup as not connected")
            self.setup()

    def setup(self):
        logging.debug("checking ports that match %s" % self.vidpid)
        ports = serial.tools.list_ports.grep(self.vidpid)
        for port in ports:
            try:
                logging.info("found Dygma Raise on %s" % port.device)
                # only open serial port if connected to FW
                if self.vidpid == RAISE_FW_VIDPID:
                    self.ser = serial.Serial(port.device, 9600, timeout = 2, write_timeout = 2)
                self.port = port.device
                self.connected = True
                return True
            except serial.serialutil.SerialException:
                self.connected = False
                return False

    def run_cmd(self, cmd, quiet=False):
        output = ""
        if not quiet:
            logging.info("> %s" % cmd)
        try:
            self.ser.write(str.encode(cmd + "\n")) # must write \n with no delay or 10% chance not receive command correctly!

            while True:
                resultLine = self.ser.readline().decode('utf-8')

                if resultLine == "\r\n" or resultLine == "\n":
                    resultLine = " "
                else:
                    resultLine = resultLine.rstrip()

                if resultLine == ".":
                    break

                if resultLine:
                    output += resultLine
                    if not quiet:
                        logging.info("< %s" % resultLine)

        except serial.serialutil.SerialException:
            logging.warning("write timeout")
            self.connected = False

        return output

