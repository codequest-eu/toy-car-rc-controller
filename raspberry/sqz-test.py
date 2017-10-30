import sys
sys.path.append('/root/miniconda3/lib/python3.4/site-packages')

from keras.models import model_from_json
import numpy as np
import time
import h5py

with open('out.json', encoding='utf-8') as net:
        model_text = net.read()
        model = model_from_json(model_text)

model.load_weights('out.h5')

image_array1 = np.zeros((1, 64, 64, 1))
image_array2 = np.ones((1, 64, 64, 1))

start_time = time.time()
steering_angle = float(model.predict(image_array1, batch_size=1))
end_time = time.time()
print('1st: ' + str(end_time - start_time))

start_time = time.time()
steering_angle = float(model.predict(image_array2, batch_size=1))
end_time = time.time()
print('2nd: ' + str(end_time - start_time))

start_time = time.time()
steering_angle = float(model.predict(image_array1, batch_size=1))
end_time = time.time()
print('3rd: ' + str(end_time - start_time))

print('angle: ' + str(steering_angle))
