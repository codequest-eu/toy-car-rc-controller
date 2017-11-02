import imutils
import itertools
import csv
import cv2
from random import random

MIDDLE_POINT = 1512.0

def preprocess_image(image):
    processed_image = image[:, :250] #TODO: even smaller part of the image?
    processed_image = imutils.rotate_bound(processed_image, 270)
    processed_image = cv2.resize(processed_image, (64, 64), cv2.INTER_AREA)
    return cv2.cvtColor(processed_image, cv2.COLOR_RGB2HSV)[:,:,2]

def load_image(image_path):
    image = cv2.imread(image_path)
    return preprocess_image(image)

def normalized_label(label):
    return label - MIDDLE_POINT

def denormalized_label(label):
    return label + MIDDLE_POINT

# prepare features and labels from saved session
def prepare_from_path(path):
    result_images = []
    result_labels = []
    with open(path + '/data.csv') as f:
        csv_data = list(csv.reader(f, delimiter=';'))

    images, labels = list(map(lambda x: load_image(path + '/' + x[3]), csv_data)), list(map(lambda x: int(x[2]), csv_data))
    for index, label in enumerate(labels):
        normalized = normalized_label(label)
        # cv2.imshow(str(label), images[index])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if abs(normalized) > 25:
            result_images.append(images[index])
            result_labels.append(normalized)

            # flipped_image = cv2.flip(images[index], 1)
            # flipped_label = 2*MIDDLE_POINT - label
            # result_images.append(flipped_image)
            # result_labels.append(flipped_label)
        elif random() < 0.55: # discard n% of stright angle data
            result_images.append(images[index])
            result_labels.append(normalized)

    return result_images, result_labels

# prepare features and labels from saved sessions
def prepare_from_paths(paths):
    all_features = []
    all_labels = []
    for path in paths:
        features, labels = prepare_from_path(path)
        all_features += features
        all_labels += labels

    return all_features, all_labels
