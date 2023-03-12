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
# PATHS = ['photos_made_by_robot_from_phone/IMG_1_1_IMG_1_2_matches.npz',     # first movement
#          'photos_made_by_robot_from_phone/IMG_2_1_IMG_2_2_matches.npz',     # first movement second series of pictures 
#          'photos_made_by_robot_from_phone/IMG_2_2_IMG_2_3_matches.npz']     # second movement second series of pictures 

# # Change depending on movement !!
# ROTATION = -(pi * 45)/180   # in radians
# ZMOVEMENT = 0.046           # in meters
# XMOVEMENT = 0.392           # in meters

# MOVEMENTS = [[XMOVEMENT, ZMOVEMENT, ROTATION],
#             [XMOVEMENT, ZMOVEMENT, ROTATION],
#             [0.071, -40.6, (pi * 45/2)/180 ]]


# Movements for photos with charuco
# MOVEMENTS = [[0.05, 0, 0]]
MOVEMENTS = [
            [-0.05, 0, 0.209],
            [-0.05, 0.05, 0],
            [-0.1, -0.05, 0],
            [-0.1, -0.05, 0],
            [-0.05, 0.05, 0.227]]


#PATHS = ['photos_made_by_phone_testing_2/IMG_1_IMG_2_matches.npz']
PATHS = ['soup_photos_full_movements/IMG_1_IMG_2_matches.npz',
        'soup_photos_full_movements/IMG_2_IMG_3_matches.npz', 
        'soup_photos_full_movements/IMG_3_IMG_4_matches.npz', 
        'soup_photos_full_movements/IMG_4_IMG_5_matches.npz']

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

    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, points1.astype(np.float64).T, points2.astype(np.float64).T)

    

def main():
    HOW_MANY_POINTS = 30

    for i in range(len(PATHS)): 
        # to jest nadpisywane i tak
        print(PATHS[i])
        (points1, points2) = matches.find_matches(PATHS[i])

        # # points from charuco board measured with gimp on 26.02. The second robot is moving in relation
        # # to the first one: 5cm to the left. Both are in distance of 30cm from the board.
        # points1 = np.array([[1500, 3399], [589,3407], [586, 3110], [881, 3113], [877, 2820], [1173, 2820]])
        # points2 = np.array([[2034, 3390], [1122, 3396], [1119, 3100], [1416, 3104], [1414, 2809], [1710, 2811]])
        # HOW_MANY_POINTS = 6

        # points1 = np.array([[1003, 3410], [107, 3412], [102, 3121], [392, 3123], [386, 2831], [677, 2834]])
        # points2 = np.array([[2000, 3419], [1093, 3428], [1090, 3135], [1385, 3137], [1383, 2842], [1677, 2844]])
        # HOW_MANY_POINTS = 6

        # points1 = np.array([[898, 3208], [105, 3227], [101, 2970], [360, 2968], [355, 2714], [612, 2711]])
        # points2 = np.array([[2083, 3803], [991, 3815], [988, 3456], [1342, 3460], [1342, 3106], [1695, 3108]])
        # HOW_MANY_POINTS = 6

        # points1 = np.array([[1984, 3404], [1990, 3154], [2228, 3153], [2260, 2827], [2109, 2717], [1468, 2595]])
        # points2 = np.array([[2405, 3513], [2408, 3256], [2662, 3299], [2693, 2956], [2529, 2823], [1902, 2640]])
        # HOW_MANY_POINTS = 6

        for j in range(HOW_MANY_POINTS):
            print(points1[j],"   ", points2[j])

        X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],points2[:HOW_MANY_POINTS,:], MOVEMENTS[i], intrinsic)
        #X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],points2[:HOW_MANY_POINTS,:], MOVEMENTS[i], intrinsic)
        X = cv2.convertPointsFromHomogeneous(X.T)
        print(X)
        #  break

if __name__ == '__main__':
    main()
  
'''
# cube in relation to the camera: (0, 0, 20)
points_photo1 = np.array(
[[0.0, -1.3, 20.0],
[0.0, 4.7, 20.0],
[6.0, 4.7, 20.0],
[6.0, -1.3, 20.0],
[0.0, -1.3, 26.0],
[0.0, 4.7, 26.0],
[6.0, 4.7, 26.0],
[6.0, -1.3, 26.0]]
)

# cube in relation to the camera: (-5, 0, 30)
points_photo2 = np.array(
[[-5.0, -1.3, 30.0],
[-5.0, 4.7, 30.0],
[1.0, 4.7, 30.0],
[1.0, -1.3, 30.0],
[-5.0, -1.3, 36.0],
[-5.0, 4.7, 36.0],
[1.0, 4.7, 36.0],
[1.0, -1.3, 36.0]]
)

# cube in relation to the camera: (-5, 0, 25)
points_photo3 = np.array(
[[-5.0, -1.3, 25.0],
[-5.0, 4.7, 25.0],
[1.0, 4.7, 25.0],
[1.0, -1.3, 25.0],
[-5.0, -1.3, 31.0],
[-5.0, 4.7, 31.0],
[1.0, 4.7, 31.0],
[1.0, -1.3, 31.0]]
)

# cube in relation to the camera: (-15, 0, 30, 12st)
points_photo4 = np.array(
[[-8.43484739 -1.3        32.46310752],
[-8.43484739  4.7        32.46310752],
[-2.56596239  4.7        31.2156345 ],
[-2.56596239 -1.3        31.2156345 ],
[-7.18737437 -1.3        38.33199251],
[-7.18737437  4.7        38.33199251],
[-1.31848937  4.7        37.08451949],
[-1.31848937 -1.3        37.08451949]]
)

# cube in relation to the camera: (0, 0, 30)
points_photo5 = np.array(
[[0.0, -1.3, 30.0],
[0.0, 4.7, 30.0],
[6.0, 4.7, 30.0],
[6.0, -1.3, 30.0],
[0.0, -1.3, 36.0],
[0.0, 4.7, 36.0],
[6.0, 4.7, 36.0],
[6.0, -1.3, 36.0]]
)

# cube in relation to the camera: (5, 0, 20)
points_photo6 = np.array(
[[5.0, -1.3, 20.0],
[5.0, 4.7, 20.0],
[11.0, 4.7, 20.0],
[11.0, -1.3, 20.0],
[5.0, -1.3, 26.0],
[5.0, 4.7, 26.0],
[11.0, 4.7, 26.0],
[11.0, -1.3, 26.0]]
)

# cube in relation to the camera: (20, 0, 25, 12 deg)
points_photo7 = np.array(
[[14.36514573 -1.3        28.61193087],
[14.36514573  4.7        28.61193087],
[20.23403072  4.7        29.85940389],
[20.23403072 -1.3        29.85940389],
[13.11767271 -1.3        34.48081586],
[13.11767271  4.7        34.48081586],
[18.98655771  4.7        35.72828888],
[18.98655771 -1.3        35.72828888]]
)

#  3,7---2,6
#  |     |
#  |     |
#  4,8---1,5

'''
