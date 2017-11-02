from continuous_task import ContinuousTask
from multiprocessing import Value
import os
from picamera import PiCamera
import time

class Capturer(ContinuousTask):

    def __init__(self):
        ContinuousTask.__init__(self, False)
        self.capture_started = Value('i', 0)
        self.directory = None
        self.start_process()

    def start(self, directory):
        self.capture_started.value = 1
        self.queue.put(('start', directory))

    def stop(self):
        self.capture_started.value = 0

    def handle_command(self):
        (command, directory) = self.get_command()
        if command == 'start':
            self.directory = directory

    def run(self):
        if self.capture_started.value == 1:
            with PiCamera(resolution=(640, 480), framerate=15) as camera:
                camera.start_preview()
                time.sleep(2)
                camera.capture_sequence(self.filenames(), use_video_port=True)

    def timestamp(self):
        return int(round(time.time() * 1000))

    def filenames(self):
        while self.capture_started.value == 1 and not self.terminated():
            yield '%s/images/%d.jpg' % (self.directory, self.timestamp())
