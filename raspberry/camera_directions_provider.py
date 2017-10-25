from picamera import PiCamera
from picamera.array import PiRGBArray
from neural_network_predictor import NeuralNetworkPredictor
import os

class CameraDirectionsProvider:

    def __init__(self):
        print("Init process %s" % str(os.getpid()))
        self.camera = None
        self.rawCapture = None
        self.stream = None
        self.predictor = NeuralNetworkPredictor()

    def __del__(self):
        print("Del process %s" % str(os.getpid()))
        if self.camera:
            self.camera.stop_preview()
            self.camera.close()

    def __iter__(self):
        return self

    def next(self):
        print("Next process %s" % str(os.getpid()))
        if not self.stream:
            self.camera = PiCamera(resolution=(640, 480), framerate=15)
            self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
            self.camera.start_preview()
            self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
        print("Want frame")
        frame = next(self.stream)
        print("Got frame")
        result = self.predictor.predict_angle(frame.array)
        print("Got from NN: %d" % result)
        self.rawCapture.truncate(0)
        return (0, result)

    def __next__(self):
        return self.next()

