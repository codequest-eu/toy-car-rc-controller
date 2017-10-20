from continuous_task import ContinuousTask
from multiprocessing import Queue
import os
import serial
import time
import sys
import serial_port

class SerialReader(ContinuousTask):

    def __init__(self):
        ContinuousTask.__init__(self, True)
        self.file = sys.stdout
        self.port = serial.Serial(serial_port.available_name(), 9600, timeout=0.1)
        self.start_process()

    def start_saving(self, directory):
        self.queue.put(('start', directory))

    def stop_saving(self):
        self.queue.put(('stop', None))

    def handle_command(self):
        (command, directory) = self.get_command()
        if command == 'start':
            self.file = open("%s/log" % directory, "w")
        elif command == 'stop':
            if self.file != sys.stdout:
                self.file.close()
            self.file = sys.stdout

    def run(self):
        read_serial = self.port.readline()
        if read_serial:
            read_serial = read_serial.strip()
            if self.file == sys.stdout or read_serial.isdigit():
                self.file.write('%d/%s\n' % (self.timestamp(), read_serial))
                self.file.flush()

    def timestamp(self):
        return int(round(time.time() * 1000))
