import os
from multiprocessing import Value, Queue
import signal
import datetime
import time
import pytz
import cherrypy
from cherrypy.process.plugins import SimplePlugin
from capturer import Capturer
from serial_reader import SerialReader
from interrupt_handler import InterruptHandler
from command_executor import CommandExecutor, Status
from route_sender import RouteSender
from replay_directions_provider import ReplayDirectionsProvider
from camera_directions_provider import CameraDirectionsProvider

class ExitPlugin(SimplePlugin):

  def __init__(self, bus, server):
    SimplePlugin.__init__(self, bus)
    self.server = server

  def exit(self):
    self.unsubscribe()
    self.server.terminate()

class CarServer(object):

    def directory_for_session(self):
        directory = "session-%s" % self.timestamp()
        images = "%s/images" % directory
        os.makedirs(images)
        return directory
    
    def __init__(self):
        self.timezone = pytz.timezone('Europe/Warsaw')
        self.capturer = Capturer()
        self.serial_reader = SerialReader()
        self.command_executor = CommandExecutor()
        self.route_sender = None
        self.started = False
        self.driving_started = False

    @cherrypy.expose
    def idle(self):
        self.command_executor.change_status(Status.IDLE)

    @cherrypy.expose
    def remote(self):
        self.command_executor.change_status(Status.REMOTE)

    @cherrypy.expose
    def learning(self):
        self.command_executor.change_status(Status.LEARNING)

    def autonomous(self):
        self.command_executor.change_status(Status.AUTONOMOUS)

    @cherrypy.expose
    def turn(self, angle):
        self.command_executor.make_turn(int(angle))

    @cherrypy.expose
    def replay(self, directory):
        self.driving_started = True
        directions = ReplayDirectionsProvider(directory)
        self.route_sender = RouteSender(self.command_executor, directions)
        self.autonomous()

    @cherrypy.expose
    def drive(self):
        self.driving_started = True
        directions = CameraDirectionsProvider()
        initialized_queue = Queue()
        self.route_sender = RouteSender(self.command_executor, directions, initialized_queue)
        print("Waiting for initialization")
        if initialized_queue.get():
            print("Initialization completed")
            self.autonomous()

    @cherrypy.expose
    def start(self):
        if self.started:
            cherrypy.response.status = 400
            return "WARNING: Session already started"
        if self.driving_started:
            cherrypy.response.status = 400
            return "WARNING: Driving in progress"

        directory = self.directory_for_session()
        self.started = True
        self.capturer.start(directory)
        self.serial_reader.start_saving(directory)
        self.remote()

        return "INFO: Session %s has been started" % directory

    @cherrypy.expose
    def stop(self):
       if not self.started and not self.driving_started:
           cherrypy.response.status = 400
           return "WARNING: Neither session nor driving started"
       if self.started:
           self.idle()
           self.cleanup()
           return "INFO: Session ended successfully"
       else:
           self.stop_driving()
           return "INFO: Driving ended successfully"

    def stop_driving(self):
        self.driving_started = False
        self.route_sender.terminate()
        self.route_sender = None

    def terminate(self):
        self.cleanup()
        self.capturer.terminate()
        self.serial_reader.terminate()

    def cleanup(self):
        if not self.started:
            return

        self.capturer.stop()
        self.serial_reader.stop_saving()
        self.started = False

    def timestamp(self):
        utc_dt = datetime.datetime.now(pytz.utc)
        loc_dt = utc_dt.astimezone(self.timezone)
        return loc_dt.strftime("%Y%m%d%H%M%S")

if __name__ == "__main__":
    car_server = CarServer()
    ExitPlugin(cherrypy.engine, car_server).subscribe()
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(car_server)
