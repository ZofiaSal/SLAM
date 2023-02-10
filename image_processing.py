from cmath import pi
from gettext import translation
import numpy as np
import cv2
import find_matches_with_superglue as matches

#Prepared beforehand with script camera_calibration/calibrate_camera.py and photos from photos_made_by_robot_from_phone:
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
YMOVEMENT = 0.392           # in meters

MOVEMENTS = [[XMOVEMENT, YMOVEMENT, ROTATION],
            [XMOVEMENT, YMOVEMENT, ROTATION],
            [0.071, -40.6, (pi * 45/2)/180 ]]



def getRotationsInXY(angle):
    Rz = np.zeros(shape = (3, 3))
    Rz[0, 0] = np.cos(angle)
    Rz[0, 1] = -np.sin(angle)
    Rz[1, 0] = np.sin(angle)
    Rz[1, 1] = np.cos(angle)
    Rz[2, 2] = 1
    
    return Rz

# returned values set the 2 photo in the center of observation
# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# distance - the change from where picture 1 was taken to where picture 2 was taken [x,y,alpha] where alpha is a rotation in XY
def calculatePoints3D(points1, points2, distance):
    
    # Calculate extrinsic matrixes.
    rotation1 = np.identity(4, dtype = np.float64)
    rotation1[:3, :3] = getRotationsInXY(-distance[2])  # TODO with minus ?
    rotation2 = np.identity(4, dtype = np.float64)

    translation1 = np.identity(4, dtype = np.float64)
    translation1[:2, 3] = [value * -1 for value in distance] [:2]
    translation2 = np.identity(4, dtype = np.float64)

    extrinsic1 = np.linalg.inv(rotation1 @ translation1)
    extrinsic2 = np.linalg.inv(rotation2 @ translation2)


    # Remove last row of Extrinsic -> (3,4).
    extrinsic1 = extrinsic1[:-1, :]
    extrinsic2 = extrinsic2[:-1, :]

    projectionMatrix1 = intrinsic @ extrinsic1
    projectionMatrix2 = intrinsic @ extrinsic2

    # TODO: Is that even needed? -> nope, doesnt work 
    points_undist1 = cv2.undistortPoints(points1.astype(np.float64), intrinsic, distortion)
    points_undist2 = cv2.undistortPoints(points2.astype(np.float64), intrinsic, distortion)
    
    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, points1.astype(np.float64).T, points2.astype(np.float64).T)

    

def main():
    HOW_MANY_POINTS = 20

    for i in range(len(PATHS)): 
        print(PATHS[i])
        (points1, points2) = matches.find_matches(PATHS[i])
        print(points1[:HOW_MANY_POINTS,:],"\n", points2[:HOW_MANY_POINTS,:])

        X = calculatePoints3D(points1[:HOW_MANY_POINTS,:],points2[:HOW_MANY_POINTS,:],MOVEMENTS[i])
        X = cv2.convertPointsFromHomogeneous(X.T)
        print(np.round(X,2))


if __name__ == '__main__':
    main()