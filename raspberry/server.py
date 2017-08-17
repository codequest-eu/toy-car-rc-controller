import os
from multiprocessing import Value
import signal
import time
import cherrypy
from capturer import Capturer
from serial_reader import SerialReader
from interrupt_handler import InterruptHandler

class CarServer(object):

    def __init__(self):
        self.terminator = None
        self.capturer = None
        self.serial_reader = None

    @cherrypy.expose
    def start(self):
        if self.terminator:
            cherrypy.response.status = 400
            return "WARNING: Session already started"
        directory = "session-%d" % timestamp()
        images = "%s/images" % directory
        os.makedirs(images)
        self.terminator = Value('i', 0)

        self.capturer = Capturer(directory, self.terminator)
        self.serial_reader = SerialReader(directory, self.terminator)

        self.capturer.start()
        self.serial_reader.start()
        return "INFO: Session %s has been started" % directory

    @cherrypy.expose
    def stop(self):
       if not self.terminator:
           cherrypy.response.status = 400
           return "WARNING: Session not started"
       self.terminator.value = 1
       self.capturer.join()
       self.serial_reader.join()

       self.terminator = None
       self.capturer = None
       self.serial_reader = None

    def timestamp(self):
        return int(round(time.time() * 1000))

if __name__ == "__main__":
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(CarServer())
