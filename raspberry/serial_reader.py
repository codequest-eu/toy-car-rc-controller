import os
import serial
import time
from multiprocessing import Process
import signal

class SerialReader(Process):

    def __init__(self, directory, terminator):
        Process.__init__(self)
        self.daemon = True
        self.directory = directory
        self.terminator = terminator

    def timestamp(self):
        return int(round(time.time() * 1000))

    def run(self):
        print("Reading from serial in process %d" % os.getpid())
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        os.chdir(self.directory)
        ser = serial.Serial('/dev/ttyACM0', 9600)
        with open("log", "w") as f:
            while self.terminator.value == 0:
                read_serial = ser.readline()
                f.write(str(self.timestamp()) + "/" +  read_serial)

