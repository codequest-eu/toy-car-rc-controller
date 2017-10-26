import imutils
import itertools
import csv
import cv2

def preprocess_image(image):
        processed_image = image[:, :320]
        processed_image = imutils.rotate_bound(processed_image, 270)
        processed_image = cv2.resize(processed_image, (64, 64), cv2.INTER_AREA)
        return cv2.cvtColor(processed_image, cv2.COLOR_RGB2HSV)[:,:,1]

def load_image(image_path):
	image = cv2.imread(image_path)
	return preprocess_image(image)

# prepare features and labels from saved session
def prepare_from_path(path):
	with open(path + '/data.csv') as f:
		csv_data = list(csv.reader(f, delimiter=';'))
	
	return list(map(lambda x: load_image(path + '/' + x[3]), csv_data)), list(map(lambda x: int(x[2]), csv_data))

# prepare features and labels from saved sessions
def prepare_from_paths(paths):
	all_features = []
	all_labels = []
	for path in paths:
		features, labels = prepare_from_path(path)
		all_features += features
		all_labels += labels

	return all_features, all_labels
