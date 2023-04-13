import cv2 as cv
import numpy as np

img = cv.imread('photos_from_realsense/im1.jpg')
# h,  w = img.shape[:2]

mtx = np.array([[929.74227726,   0.,         687.25873423],
 [  0.,         927.24844324, 366.49210902],
 [  0.,           0.,           1.        ]])
dist = np.array([[ 0.20065356, -1.21660056,  0.00855403 , 0.00677988 , 1.90940938]])

# newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

dst = cv.undistort(img, mtx, dist)
# crop the image
# x, y, w, h = roi
# dst = dst[y:y+h, x:x+w]
cv.imwrite('photos_from_realsense/undist1.jpg', dst)