from continuous_task import ContinuousTask
from multiprocessing import Queue
import os
import serial
import time
import sys

class SerialReader(ContinuousTask):

    def __init__(self):
        ContinuousTask.__init__(self)
        self.file = sys.stdout
        self.port = serial.Serial('/dev/ttyACM0', 9600)

    def start_saving(self, directory):
        self.queue.put(('start', directory))

    def stop_saving(self):
        self.queue.put(('stop', None))

    def handle_command(self):
        (command, directory) = self.get_command()
        if command == 'start':
            os.chdir(directory)
            self.file = open("log", "w")
        elif command == 'stop':
            if self.file != sys.stdout:
                self.file.close()
            self.file = sys.stdout

    def run(self):
        read_serial = self.port.readline()
        self.file.write(str(self.timestamp()) + "/" +  read_serial)

    def timestamp(self):
        return int(round(time.time() * 1000))
