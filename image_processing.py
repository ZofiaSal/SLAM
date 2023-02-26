from cmath import pi
from gettext import translation
import numpy as np
import cv2
import find_matches_with_superglue as matches

# Prepared beforehand with script camera_calibration/calibrate_camera.py and photos from photos_made_by_robot_from_phone:
# intrinsic = np.matrix([[3.25469171e+03, 0.00000000e+00, 1.97045738e+03],
#  [0.00000000e+00, 3.27559539e+03, 1.35368028e+03],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype = np.float64)
intrinsic = np.matrix([[3.10055067e+03, 0.00000000e+00, 1.53884049e+03],
 [0.00000000e+00, 3.09458047e+03, 2.01598760e+03],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype = np.float64)

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
        # [[ 0.04404553 -0.18982083 -0.3046698 ]]
        # [[ 0.12955368 -0.19080615 -0.30520441]]
        # [[ 0.1298415  -0.1631898  -0.30522335]]
        # [[ 0.10179917 -0.16291434 -0.3041004 ]]
        # [[ 0.10178287 -0.13509803 -0.30293018]]
        # [[ 0.07423874 -0.13520715 -0.3029675 ]]

        points1 = np.array([[1003, 3410], [107, 3412], [102, 3121], [392, 3123], [386, 2831], [677, 2834]])
        points2 = np.array([[2000, 3419], [1093, 3428], [1090, 3135], [1385, 3137], [1383, 2842], [1677, 2844]])
        HOW_MANY_POINTS = 6
        # [[ 0.09703354 -0.2053685  -0.32642544]]
        # [[ 0.18896063 -0.20818205 -0.3300166 ]]
        # [[ 0.18909123 -0.17841028 -0.32936547]]
        # [[ 0.15893977 -0.17771208 -0.32770712]]
        # [[ 0.15891096 -0.14776335 -0.3264138 ]]
        # [[ 0.12933879 -0.14757115 -0.32544055]]

        for j in range(HOW_MANY_POINTS):
            print(points1[j],"   ", points2[j])

        X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],points2[:HOW_MANY_POINTS,:], [0.1, 0, 0], intrinsic)
        X = cv2.convertPointsFromHomogeneous(X.T)
        print(X)
        break

if __name__ == '__main__':
    main()