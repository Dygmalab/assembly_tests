import logging
import serial, time
import serial.tools.list_ports
RAISE_VIDPID = '1209:2201'

class SerialPlug():

    def __init__(self):
        self.setup()

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

