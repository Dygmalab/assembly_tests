import subprocess
import sys
import logging

try:
    import usb.core
    import usb.util
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyusb'])
finally:
    import usb.core
    import usb.util

def get_serial():
    dev = usb.core.find(idProduct=0x2201)
    logging.warning(dev)
    try:
        serial = usb.util.get_string( dev, dev.iSerialNumber)
        logging.warning("serial # %s" % serial)
        return serial
    except Exception as e:
        logging.warning("fetch serial failed: %s" % e)
