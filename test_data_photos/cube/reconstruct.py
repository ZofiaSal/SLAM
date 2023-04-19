from cmath import pi
import subprocess
import numpy as np
import os
import cv2

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

def calculatePointsFromPaths():
    points3D = []

    for i in range(1): 
        try :
            points1 = np.array([[594, 429], [593, 97], [359, 135], [360, 419],
                                [744, 412], [745, 157], [532, 182], [532, 406]])  

            points2 = np.array([[524, 415], [523, 147], [251, 146], [251, 416],
                                [553, 402], [553, 194], [342, 193], [342, 403]])

            HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

            POINTS = triangulatePoints(points1[:HOW_MANY_POINTS,:],
                                points2[:HOW_MANY_POINTS,:], 
                                MOVEMENTS[i])
            POINTS = cv2.convertPointsFromHomogeneous(POINTS.T)
            POINTS_SHAPED = POINTS[:, 0, :]

            for j in range(HOW_MANY_POINTS):
                POINTS_SHAPED[j] = changeCoordinates(POINTS_SHAPED[j], MOVEMENTS[i])

            points3D.append(np.array(POINTS_SHAPED))
        except Exception as e:
            print(e)
            continue
    
    return points3D

def main():
    print(calculatePointsFromPaths())

if __name__ == '__main__':
    main()