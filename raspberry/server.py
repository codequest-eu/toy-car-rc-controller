import os
from multiprocessing import Value
import signal
import datetime
import time
import pytz
import cherrypy
from cherrypy.process.plugins import SimplePlugin
from capturer import Capturer
from serial_reader import SerialReader
from interrupt_handler import InterruptHandler

class ExitPlugin(SimplePlugin):

  def __init__(self, bus, server):
    SimplePlugin.__init__(self, bus)
    self.server = server

  def exit(self):
    self.unsubscribe()
    self.server.cleanup()

class CarServer(object):

    def __init__(self):
        self.timezone = pytz.timezone('Europe/Warsaw')
        self.terminator = Value('i', 1)
        self.capturer = None
        self.serial_reader = None

    @cherrypy.expose
    def start(self):
        if self.terminator.value == 0:
            cherrypy.response.status = 400
            return "WARNING: Session already started"
        directory = "session-%s" % self.timestamp()
        images = "%s/images" % directory
        os.makedirs(images)
        self.terminator.value = 0

        self.capturer = Capturer(directory, self.terminator)
        self.serial_reader = SerialReader(directory, self.terminator)

        self.capturer.start()
        self.serial_reader.start()
        return "INFO: Session %s has been started" % directory

    @cherrypy.expose
    def stop(self):
       if self.terminator.value == 1:
           cherrypy.response.status = 400
           return "WARNING: Session not started"
       self.cleanup()
       return "INFO: Session ended successfully"

    def cleanup(self):
        if self.terminator.value == 1:
            return
        self.terminator.value = 1
        self.capturer.join()
        self.serial_reader.join()

        self.capturer = None
        self.serial_reader = None 

    def timestamp(self):
        utc_dt = datetime.datetime.now(pytz.utc)
        loc_dt = utc_dt.astimezone(self.timezone)
        return loc_dt.strftime("%Y%m%d%H%M%S")

if __name__ == "__main__":
    car_server = CarServer()
    ExitPlugin(cherrypy.engine, car_server).subscribe()
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(car_server)