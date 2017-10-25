import cv2
import time
import imutils

image = cv2.imread('images/1508940361283.jpg')

start_time = time.time()
image = image[:, :320]
image = imutils.rotate_bound(image, 270)
image = cv2.resize(image, (64, 64), cv2.INTER_AREA)
image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)[:,:,1]
end_time = time.time()
print('transform time: ' + str(end_time - start_time))

cv2.imwrite('result.png', image)

