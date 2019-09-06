import logging
import serial, time
import serial.tools.list_ports
RAISE_VIDPID = '1209:2201'

class SerialPlug():

    def __init__(self):
        self.connected = False
        self.ser = None

    def is_connected(self):
        return self.connected

    def get_status_message(self):
        if self.connected:
            return "connected on port %s" % self.port
        else:
            return("trying to connect to a Raise...")

    def check_serial_status(self):
        if self.connected:
            # try a write
            self.run_cmd("", quiet=True)
        else:
            # otherwise try to setup
            self.setup()

    def setup(self):
        ports = serial.tools.list_ports.grep(RAISE_VIDPID)
        for port in ports:
            try:
                logging.info("found Dygma Raise on %s" % port.device)
                self.ser = serial.Serial(port.device, 9600, timeout = 1, write_timeout = 1)
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

