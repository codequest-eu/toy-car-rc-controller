import os
from picamera import PiCamera
import time
from multiprocessing import Process
import signal

class Capturer(Process):

    def __init__(self, directory, terminator):
        Process.__init__(self)
        self.directory = directory
        self.terminator = terminator
        self.daemon = True

    def timestamp(self):
        return int(round(time.time() * 1000))

    def filenames(self):
        while self.terminator.value == 0:
            yield 'images/%d.jpg' % self.timestamp()

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        os.chdir(self.directory)
        with PiCamera(resolution=(640, 480), framerate=15) as camera:
            camera.start_preview()
            time.sleep(2)
            camera.capture_sequence(self.filenames(), use_video_port=True)

