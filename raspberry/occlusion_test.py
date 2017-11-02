import numpy as np
import cv2
import sys
import csv

from keras.models import model_from_json
from preprocess_dataset import preprocess_image, denormalized_label

OCCLUSION_RADIUS=1
np.set_printoptions(threshold=np.nan, precision=1, suppress=True)

if len(sys.argv) < 2:
    image_path = 'session-5/images/1509378626651.jpg'
else:
    image_path = sys.argv[1]

def load_model():
    print('loading model')
    with open('out.json', encoding='utf-8') as net:
        model_text = net.read()
        model = model_from_json(model_text)
    print('model loaded, loading weights')
    model.load_weights('out.h5')
    print('weights loaded')

    return model

def predict(image, model):
    result = float(model.predict(image.reshape(1, 64, 64, 1), batch_size=1))
    return denormalized_label(result)

def occlude(image, x, y):
    occluded = np.copy(image)
    occluded[y - OCCLUSION_RADIUS:y + OCCLUSION_RADIUS + 1, x - OCCLUSION_RADIUS:x + OCCLUSION_RADIUS + 1] = 0
    # cv2.imshow('preview', occluded)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return occluded

def process_image(image, model):
    image = preprocess_image(image)
    score = np.zeros(image.shape)
    original_score = predict(image, model)

    for y in range(0, len(image)):
        for x in range(0, len(image[0])):
            occluded_image = occlude(image, x, y)
            result = predict(occluded_image, model)
            score[y - OCCLUSION_RADIUS:y + OCCLUSION_RADIUS + 1, x - OCCLUSION_RADIUS:x + OCCLUSION_RADIUS + 1] += abs(original_score - result)

    max_score = np.amax(score)
    score *= (1.0 / max_score)
    return score

    # print(score)
    # score = cv2.resize(score, (256, 256), cv2.INTER_AREA)

def process_from_path(path, model):
    with open(path + '/data.csv') as f:
        csv_data = list(csv.reader(f, delimiter=';'))

    images = list(map(lambda x: cv2.imread(path + '/' + x[3]), csv_data))

    images_count = len(images)
    for idx, image in enumerate(images):
        print(str(idx) + '/' + str(images_count))
        score = process_image(image, model) * 255.0
        # cv2.imshow('score', score)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite('test_video/' + str(idx) + '.png', score)

model = load_model()
process_from_path('session-5', model)
# image = cv2.imread(image_path)
# process_image(image, model)
