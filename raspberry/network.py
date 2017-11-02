import sys
sys.path.append('/root/miniconda3/lib/python3.4/site-packages')

from keras.models import model_from_json
from keras.models import load_model
from keras.optimizers import Adam
import numpy as np
import time
import h5py
import cv2
import imutils

print('loading model')
with open('out.json', encoding='utf-8') as net:
        model_text = net.read()
        model = model_from_json(model_text)
print('model loaded, loading weights')
model.load_weights('out.h5')
print('weights loaded')

def preprocess_image(image):
     image = image[:, :320]
     image = imutils.rotate_bound(image, 270)
     image = cv2.resize(image, (64, 64), cv2.INTER_AREA)
     return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:,:,1]

def predict_angle(image):
    image = preprocess_image(image)
    result = float(model.predict(image.reshape(1, 64, 64, 1), batch_size=1))
    interpolated = 1470 + result * 490
    return int(interpolated)

#image = cv2.imread('1508940361283.jpg')
#print(predict_angle(image))

