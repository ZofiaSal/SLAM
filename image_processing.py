from cmath import pi
from gettext import translation
import numpy as np
import cv2
import find_matches_with_superglue as matches

# Prepared beforehand with script camera_calibration/calibrate_camera.py and photos from photos_made_by_robot_from_phone:
intrinsic = np.matrix([[3.25469171e+03, 0.00000000e+00, 1.97045738e+03],
 [0.00000000e+00, 3.27559539e+03, 1.35368028e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype = np.float64)

distortion = np.matrix([[ 2.46232395e-01, -2.44055557e+00, -2.25038168e-02, -1.39744208e-03,
   5.37815833e+00]], dtype = np.float64)

# Change depending on desired photos!!
# This is the output of SuperGlue (description how to get its: feature_points/README.md)
PATHS = ['photos_made_by_robot_from_phone/IMG_1_1_IMG_1_2_matches.npz',     # first movement
         'photos_made_by_robot_from_phone/IMG_2_1_IMG_2_2_matches.npz',     # first movement second series of pictures 
         'photos_made_by_robot_from_phone/IMG_2_2_IMG_2_3_matches.npz']     # second movement second series of pictures 

# Change depending on movement !!
ROTATION = -(pi * 45)/180   # in radians
XMOVEMENT = 0.046           # in meters
ZMOVEMENT = 0.392           # in meters

MOVEMENTS = [[XMOVEMENT, ZMOVEMENT, ROTATION],
            [XMOVEMENT, ZMOVEMENT, ROTATION],
            [0.071, -40.6, (pi * 45/2)/180 ]]

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

    extrinsicCamera2 = [[np.cos(angle), np.sin(angle), 0, -distance[0]],
                        [- np.sin(angle), np.cos(angle), 0, 0],
                        [0, 0, 1, -distance[1]]]

    projectionMatrix1 = intrinsicCamera @ extrinsicCamera1
    projectionMatrix2 = intrinsicCamera @ extrinsicCamera2

    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, points1.astype(np.float64).T, points2.astype(np.float64).T)

    

# 13.6 -2.7
def main():
    HOW_MANY_POINTS = 35

    for i in range(len(PATHS)): 
        # to jest nadpisywane i tak
        # print(PATHS[i])
        # (points1, points2) = matches.find_matches(PATHS[i])

        # points from charuco board measured with gimp on 26.02. The second robot is moving in relation
        # to the first one: 5cm to the left. Both are in distance of 30cm from the board.
        # What is wrong? The z value is correct but wrong sign???
        # The y value is moved(!) by 5cm (sign is correct)
        # The x value is omved(!) by 4 cm. 
        # Expected result:
        # [0.0,   -0.138, 0.30]
        # [0.085, -0.138, 0.30]
        # [0.085, -0.11,  0.30]
        # [0.06,  -0.11,  0.30]
        # [0.06,  -0.07,  0.30]
        # [0.029, -0.07,  0.30]
        # Difference:
        # [0.04,  -0.051, 0]
        # [0.044, -0.052, 0.01]
        # [0.044, -0.053, 0.01]
        # [0.04,  -0.053, 0]
        # [0.04,  -0.065, 0]
        # [0.045, -0.065, 0]
        points1 = np.array([[1500, 3399], [589,3407], [586, 3110], [881, 3113], [877, 2820], [1173, 2820]])
        points2 = np.array([[2034, 3390], [1122, 3396], [1119, 3100], [1416, 3104], [1414, 2809], [1710, 2811]])
        HOW_MANY_POINTS = 6

        for j in range(HOW_MANY_POINTS):
            print(points1[j],"   ", points2[j])

        X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],points2[:HOW_MANY_POINTS,:], [0.05, 0, 0], intrinsic)
        X = cv2.convertPointsFromHomogeneous(X.T)
        print(X)
        break

if __name__ == '__main__':
    main()