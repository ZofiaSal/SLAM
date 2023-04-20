from cmath import pi
import subprocess
import sys
import numpy as np
import os
import cv2
import argparse

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

HOW_MANY_POINTS_DEFAULT = 1000

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


def changeCoordinates(point, movement):
    angle = - movement[2]
    x_translation = - movement[0]
    z_translation = - movement[1]
    Rxz = np.array([[np.cos(angle), 0, -np.sin(angle)],
                    [0, 1, 0],
                    [np.sin(angle), 0, np.cos(angle)]])

    # Apply the rotation matrix to point P
    point_rotated = np.dot(Rxz, point)

    # Translate the coordinates of P by x and z
    return point_rotated + np.array([x_translation, 0, z_translation])


MOVEMENTS = np.array([[- 6., - 6.8, - pi / 6]])


# Create the parser
parser = argparse.ArgumentParser(description='3d reconstruction')

# Add the arguments
parser.add_argument('--data', type=str, help='Data set directory name')

# Parse the arguments
args = parser.parse_args()
data_set = args.data

# File needs to be called points_pairs.py 
# and have a variable called points which is an array of pairs (array1, array2) where array1 are points from first image and array2 are points from second image.
def calculatePointsFromPaths(directory = data_set):
    points3D = []

    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_path + "/test_data_sets/" + directory + "/handmade_matches")
    import points_pairs as pp  

    sys.path.append(current_path + "/test_data_sets/" + directory + "/source_photos")
    import movement 
   
    MOVEMENTS = movement.MOVEMENTS

    points_sets = pp.points 

    for i in range(len(points_sets)): 
        try :
            (points1, points2) = points_sets[i]
            if points1.size != points2.size:
                raise Exception("The number of points in the two images is not the same")

            HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

            POINTS = triangulatePoints(points1[:HOW_MANY_POINTS,:],
                                points2[:HOW_MANY_POINTS,:], 
                                MOVEMENTS[i]) 
            POINTS = cv2.convertPointsFromHomogeneous(POINTS.T)
            POINTS_SHAPED = POINTS[:, 0, :]

            for j in range(HOW_MANY_POINTS):
                POINTS_SHAPED[j] = changeCoordinates(POINTS_SHAPED[j], MOVEMENTS[0])

            points3D.append(np.array(POINTS_SHAPED))
        except Exception as e:
            print("in test number " + str(i) + " occured an error: " + str(e))
            continue
    
    return points3D

def main():
    print(calculatePointsFromPaths())

if __name__ == '__main__':
    main()