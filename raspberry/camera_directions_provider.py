from picamera import PiCamera
from picamera.array import PiRGBArray
from neural_network_predictor import NeuralNetworkPredictor

class CameraDirectionsProvider:

    def __init__(self):
        self.camera = PiCamera(resolution=(640, 480), framerate=15)
        rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.camera.start_preview()
        self.stream = self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
        self.predictor = NeuralNetworkPredictor()

    def __del__(self):
        self.camera.stop_preview()
        self.camera.close()

    def __iter__(self):
        return self

    def next(self):
        frame = next(self.stream)
        return (0, self.predictor.predict(frame.array))

    def __next__(self):
        return self.next()

