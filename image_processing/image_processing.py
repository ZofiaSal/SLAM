from cmath import pi
from gettext import translation
import numpy as np
import cv2

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

# Change depending on movement !!
ROTATION = -(pi * 45)/180   # in radians
ZMOVEMENT = 0.046           # in meters
XMOVEMENT = 0.392           # in meters

MOVEMENTS = []
for i in range(12):
    movement = [XMOVEMENT, ZMOVEMENT, ROTATION]
    MOVEMENTS.append(movement)

# Change depending on desired photos!!
# This is the output of SuperGlue (description how to get its: feature_points/README.md)
PATHS = [   
            './circle_photos_matches/photo00_photo01_matches.npz',
            './circle_photos_matches/photo01_photo02_matches.npz',
            './circle_photos_matches/photo02_photo03_matches.npz',
            './circle_photos_matches/photo03_photo04_matches.npz',
            './circle_photos_matches/photo04_photo05_matches.npz',
            './circle_photos_matches/photo05_photo06_matches.npz',
            './circle_photos_matches/photo06_photo07_matches.npz',
            './circle_photos_matches/photo07_photo08_matches.npz',
            './circle_photos_matches/photo08_photo09_matches.npz',
            './circle_photos_matches/photo09_photo10_matches.npz',
            './circle_photos_matches/photo10_photo11_matches.npz',
            './circle_photos_matches/photo11_photo12_matches.npz'
        ]

K = np.array([
    [1000, 0, 0],
    [0, 1000, 0],
    [0, 0, 1]])

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# distance - the change from where picture 1 was taken to where picture 2 was taken [x,z,alpha] where alpha is a clockwise rotation in XY
def calculatePoints3D(points1, points2, distance, intrinsicCamera = K):
    angle = distance[2]
    extrinsicCamera1 = [[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0]]

    extrinsicCamera2 = [[np.cos(angle),     0,       np.sin(angle),  -distance[0]],
                        [0,                 1,      0,              0           ],
                        [-np.sin(angle),   0,      np.cos(angle),  -distance[1]]]

    projectionMatrix1 = intrinsicCamera @ extrinsicCamera1
    projectionMatrix2 = intrinsicCamera @ extrinsicCamera2

    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, 
                                 points1.astype(np.float64).T, 
                                 points2.astype(np.float64).T)

def extract_matches(path):
    data = np.load(path)
    matches = data['matches']
    keypoints0 = data['keypoints0']
    keypoints1 = data['keypoints1']
    points0 = keypoints0[matches != -1]
    points1 = keypoints1[matches[matches != -1]]
    if points0.size < 8 or points1.size < 8:
        print("Too few points to produce fundamental matrix.")
    else:
        return points0, points1

HOW_MANY_POINTS_DEFAULT = 8

def main():
    for i in range(len(PATHS)): 
        print(PATHS[i])
        (points1, points2) = extract_matches(PATHS[i])
        HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

        for j in range(HOW_MANY_POINTS):
            print(points1[j],"   ", points2[j])

        points1 = np.array([[506, 404], [505, 188], [285, 186], [286, 405], [534, 395], [534, 220], [356, 219], [356, 396]])
        points2 = np.array([[323, 405], [322, 187], [105, 187], [104, 404], [386, 396], [386, 219], [207, 218], [207, 396]])
        MOVEMENTS = [[0.05, 0, 0]]

        X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],
                              points2[:HOW_MANY_POINTS,:], 
                              MOVEMENTS[i], cameraMatrix)
        X = cv2.convertPointsFromHomogeneous(X.T)
        print(X)
        break


if __name__ == '__main__':
    main()
