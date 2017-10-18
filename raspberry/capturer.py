from continuous_task import ContinuousTask
import os
from picamera import PiCamera
import time

class Capturer(ContinuousTask):

    def __init__(self):
        ContinuousTask.__init__(self, False)
        self.start_process()

    def start(self, directory):
        self.queue.put(('start', directory))

    def stop(self):
        self.queue.put(('stop', None))

    def handle_command(self):
        (command, directory) = self.get_command()
        if command == 'start':
            os.chdir(directory)
            self.started = True
        elif command == 'stop':
            self.started = False

    def run(self):
        if self.started:
            with PiCamera(resolution=(640, 480), framerate=15) as camera:
                camera.start_preview()
                time.sleep(2)
                camera.capture_sequence(self.filenames(), use_video_port=True)

    def timestamp(self):
        return int(round(time.time() * 1000))

    def filenames(self):
        while self.started and not terminated():
            yield 'images/%d.jpg' % self.timestamp()
