from cmath import pi
import numpy as np
import cv2
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

# Change depending on movement !!
ROTATION = pi / 8   # in radians
XMOVEMENT = 0.009           # in meters
ZMOVEMENT = 0.046           # in meters

MOVEMENTS = []
for i in range(16):
    movement = [XMOVEMENT, ZMOVEMENT, ROTATION]
    MOVEMENTS.append(movement)

# Change depending on desired photos!!
# This is the output of SuperGlue (description how to get its: feature_points/README.md)
PATHS = [   
            './test_data_sets/circle_with_chess/pairs_data/photo_01_2023-04-16_photo_02_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_02_2023-04-16_photo_03_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_03_2023-04-16_photo_04_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_04_2023-04-16_photo_05_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_05_2023-04-16_photo_06_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_06_2023-04-16_photo_07_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_07_2023-04-16_photo_08_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_08_2023-04-16_photo_09_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_09_2023-04-16_photo_10_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_10_2023-04-16_photo_11_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_11_2023-04-16_photo_12_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_12_2023-04-16_photo_13_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_13_2023-04-16_photo_14_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_14_2023-04-16_photo_15_2023-04-16_matches.npz',
            './test_data_sets/circle_with_chess/pairs_data/photo_15_2023-04-16_photo_16_2023-04-16_matches.npz',
        ]

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# movement - the change from where picture 1 was taken to where picture 2 was taken [x,z,alpha] where alpha is a clockwise rotation in XY
def triangulatePoints(points1, points2, movement, intrinsicCamera = cameraMatrix):
    angle = movement[2]

    # R[I|-C]
    extrinsicCamera1 = [[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0]]

    extrinsicCamera2 = [[np.cos(angle),     0,       np.sin(angle),  -movement[0]],
                        [0,                 1,      0,              0           ],
                        [-np.sin(angle),   0,      np.cos(angle),  -movement[1]]]

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

HOW_MANY_POINTS_DEFAULT = 20

def calculatePoints3D(points1, points2, movement):
    HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

    X = triangulatePoints(points1[:HOW_MANY_POINTS,:],
                            points2[:HOW_MANY_POINTS,:], 
                            movement)
    X = cv2.convertPointsFromHomogeneous(X.T)
    
    X *= 100
    X_formatted = [[format(number, '.4f') for number in row] for row in X[:, 0, :]]

    for i in range(len(X_formatted)):
        print(X_formatted[i])

def debugImage(im):
    img1 = cv2.imread('./test_data_sets/circle_with_chess/photo_06_2023-04-16.jpg')
    img2 = cv2.imread('./test_data_sets/circle_with_chess/photo_07_2023-04-16.jpg')

    (points1, points2) = extract_matches(PATHS[im])
    HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

    for i in range(len(points1)):
        x = int(points1[i][0])
        y = int(points1[i][1])
        cv2.circle(img1, (x, y), 5, (0,255,0), -1)
        cv2.putText(img1, str(i) + ":" + str(x) + "," + str(y), (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        
        x = int(points2[i][0])
        y = int(points2[i][1])
        cv2.circle(img2, (x, y), 5, (0,255,0), -1)
        cv2.putText(img2, str(i) + ":" + str(x) + "," + str(y), (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

    cv2.imwrite('img1.jpg', img1)
    cv2.imwrite('img2.jpg', img2)


def calculatePointsFromPaths(PATHS):
    for i in range(len(PATHS)): 
        if i == 5:
            print(PATHS[i])
            debugImage(i)
            (points1, points2) = extract_matches(PATHS[i])
            HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

            X = triangulatePoints(points1[:HOW_MANY_POINTS,:],
                                points2[:HOW_MANY_POINTS,:], 
                                MOVEMENTS[i])
            X = cv2.convertPointsFromHomogeneous(X.T)
            X *= 100
            X_formatted = [[format(number, '.4f') for number in row] for row in X[:, 0, :]]

            for i in range(len(X_formatted)):
                print(X_formatted[i])

def main():
    # points1 = np.array([[1069, 416], [1080, 410], [772, 401], [732, 406], [1069, 109], [1080, 136], [772, 172], [732, 152], ])
    # points2 = np.array([[906, 397], [884, 393], [657, 393], [657, 396], [907, 190], [884, 205], [657, 206], [657, 192], ])
    # # MOVEMENTS = [[12.5, 0.2, 30 * pi / 180]]
    # MOVEMENTS = [[-0.10, -0.08, -30 * pi / 180]]

    # calculatePoints3D(points1, points2, MOVEMENTS[0])

    calculatePointsFromPaths(PATHS)

if __name__ == '__main__':
    main()
