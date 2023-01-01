import signal
import numpy as np
import sys
import serial
import time
import threading
from PyQt5 import QtCore


def openSerial(port, baud):
    serialport = serial.serial_for_url(port, do_not_open=True)
    serialport.baudrate = baud
    serialport.parity = serial.PARITY_NONE
    serialport.stopbits=serial.STOPBITS_ONE
    serialport.bytesize=serial.EIGHTBITS
    serialport.dsrdtr= True
    serialport.dtr = True
    
    try:
        serialport.open()
    except serial.SerialException as e:
        sys.stderr.write("Could not open serial port {}: {}\n".format(serialport.name, e))
        raise

    return serialport


class SerialInterface(QtCore.QObject):
    messageChanged = QtCore.pyqtSignal(str)
    
    def __init__(self, port, baud=115200):
        super().__init__()
        self.status_time = time.time()
        self.serialport = openSerial(port, baud)
        self.m_state = None
        self.m_pos = None
        self.startReadThread()

    
    def startReadThread(self):
        self.read_thread = threading.Thread(target=self.read)
        self.read_thread.start()

    def read(self):
        while True:
            message = self.serialport.read()
            try:
                message = str(message, 'utf8')
            except UnicodeDecodeError:
                print("Failed to decode", message)
                return
            if message == '':
                return
            self.messageChanged.emit(message)


    def write(self, data):
        self.serialport.write(bytes(data,"utf-8"))
        self.serialport.flush()


    def reset(self):
        print("reset\r")
        self.serialport.dtr = False
        time.sleep(.5)
        self.serialport.dtr = True