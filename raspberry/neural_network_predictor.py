import sys
sys.path.append('/root/miniconda3/lib/python3.4/site-packages')

from keras.models import model_from_json
from keras.models import load_model
import cv2
import imutils

class NeuralNetworkPredictor:

    def __init__(self):
        self.model = None

    def preprocess_image(self, image):
        image = image[:, :320]
        image = imutils.rotate_bound(image, 270)
        image = cv2.resize(image, (64, 64), cv2.INTER_AREA)
        return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:,:,1]

    def predict_angle(self, image):
        if not self.model:
            print('loading model')
            with open('out.json', encoding='utf-8') as net:
                model_text = net.read()
                self.model = model_from_json(model_text)
            print('model loaded, loading weights')
            self.model.load_weights('out.h5')
            print('weights loaded')
            print('d')
        image = self.preprocess_image(image)
        result = float(self.model.predict(image.reshape(1, 64, 64, 1), batch_size=1))
        interpolated = 1470 + result * 490
        return int(interpolated)

