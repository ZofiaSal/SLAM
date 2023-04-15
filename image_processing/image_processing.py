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
# movement - the change from where picture 1 was taken to where picture 2 was taken [x,z,alpha] where alpha is a clockwise rotation in XY
def calculatePoints3D(points1, points2, movement, intrinsicCamera = K):
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
    print("extrinsicCamera2:\n", extrinsicCamera2)

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

def calculate(points1, points2, movement):
    HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

    print("points1:\n", points1)
    print("points2:\n", points2)
    print("movement:\n", movement)

    X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],
                            points2[:HOW_MANY_POINTS,:], 
                            movement, cameraMatrix)
    X = cv2.convertPointsFromHomogeneous(X.T)
    
    X *= 100
    X_formatted = [[format(number, '.4f') for number in row] for row in X[:, 0, :]]
    print("CALCULATE")
    for i in range(len(X_formatted)):
        print(X_formatted[i])

def main():

    print("TUTAJ")

    points1 = np.array([[1069, 416], [1080, 410], [772, 401], [732, 406], [1069, 109], [1080, 136], [772, 172], [732, 152], ])
    points2 = np.array([[906, 397], [884, 393], [657, 393], [657, 396], [907, 190], [884, 205], [657, 206], [657, 192], ])
    # MOVEMENTS = [[-12.5, -0.2, -30 * pi / 180]]
    MOVEMENTS = [[-0.10, -0.08, -30 * pi / 180]]

    calculate(points1, points2, MOVEMENTS[0])

    # for i in range(len(PATHS)): 
    #     print(PATHS[i])
    #     (points1, points2) = extract_matches(PATHS[i])
    #     HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

    #     # for j in range(HOW_MANY_POINTS):
    #     #     print(points1[j],"   ", points2[j])

    #     points1 = np.array([
    #         [477, 404], [476, 188], [256, 186], [256, 405], 
    #         [511, 395], [510, 220], [332, 219], [332, 396]
    #         ])
        
    #     points2 = np.array([
    #         [293, 405], [293, 186], [76, 187], [76, 404],
    #         [362, 396], [362, 219], [184, 219], [184, 396]
    #     ])

    #     MOVEMENTS = [[0.05, 0, 0]]

    #     X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],
    #                           points2[:HOW_MANY_POINTS,:], 
    #                           MOVEMENTS[i], cameraMatrix)
    #     X = cv2.convertPointsFromHomogeneous(X.T)
    #     print("from calculate:")
    #     print(X[0])
    #     break

    # for i in range(len(PATHS)): 
    #     print(PATHS[i])
    #     (points1, points2) = extract_matches(PATHS[i])
    #     HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

    #     points1 =np.array([[906, 397], [884, 393], [657, 396], [657, 393], [907, 190], [884, 205], [657, 192], [657, 206]])
    #     points2 = np.array([[1069, 416], [1080, 410], [772, 401], [732, 406], [1069, 109], [1080, 136], [772, 172], [732, 152]])

    #     MOVEMENTS = [[0.1, 0.08, 30 * pi / 180]]

    #     points1 =np.array([[906, 397], [884, 393], [657, 396], [657, 393], [907, 190], [884, 205], [657, 192], [657, 206]])
    #     points2 = np.array([[584, 410], [593, 404], [245, 411], [293, 405], [584, 133], [592, 159], [245, 131], [293, 157]])

    #     MOVEMENTS = [[0.1, 0.08, 0]]

    #     points1 = np.array([
    #         [906, 397], [884, 393], [657, 393], [657, 396], 
    #         [907, 190], [884, 205], [657, 206], [657, 192]])

    #     points2 = np.array([
    #         [584, 410], [593, 404], [293, 405], [245, 411], 
    #         [582, 133], [590, 159], [293, 157], [245, 131]])

    #     X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],
    #                           points2[:HOW_MANY_POINTS,:], 
    #                           MOVEMENTS[i], cameraMatrix)
    #     X = cv2.convertPointsFromHomogeneous(X.T)
        
    #     X *= 100
    #     X_formatted = [[format(number, '.4f') for number in row] for row in X[:, 0, :]]

    #     for i in range(len(X_formatted)):
    #         print(X_formatted[i])

    #     calculate(points1, points2, MOVEMENTS[0])
        
    #     break


if __name__ == '__main__':
    main()
