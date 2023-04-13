import cv2 # should be 4.7
import glob
import matplotlib.pyplot as plt
import cv2.aruco as aruco
import numpy as np

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

def produce_cube_points(x, z):
    y = 1.3
    A = np.array([[x, y, z],
                  [x, y -  6., z],
                  [x - 6., y -  6., z],
                  [x - 6., y, z],
                  [x, y, z + 6.],
                  [x, y -  6., z + 6.],
                  [x - 6., y -  6., z + 6.],
                  [x - 6., y, z + 6.]])
    return A

# description of photos: alphabetically
points3dOnCube = np.array([produce_cube_points(0., 20.),
                          produce_cube_points(5., 20.),
                          produce_cube_points(10., 20.),
                          produce_cube_points(15., 20.),
                          produce_cube_points(-5., 20.),
                          produce_cube_points(-10., 20.),
                          produce_cube_points(0., 25.),
                          produce_cube_points(5., 25.),
                          produce_cube_points(10., 25.),
                          produce_cube_points(15., 25.),
                          produce_cube_points(-5., 25.),
                          produce_cube_points(-10., 25.),
                          produce_cube_points(-15., 25.),
                          produce_cube_points(0., 30.),
                          produce_cube_points(5., 30.),
                          produce_cube_points(-5., 30.),
                          [[12.3, 1.3, 23.6],
                           [12.3, -4.7, 23.6],
                           [14.8, 1.3, 28.7],
                           [14.8, -4.7, 28.7],
                           [9.6, 1.3, 31.5],
                           [9.6, -4.7, 31.5],
                           [6.3, 1.3, 23.2],
                           [6.3, -4.7, 23.2]
                           ],
                          [[-8.4, 1.3, 29.8],
                           [-8.4, -4.7, 29.8],
                           [-3.3, 1.3, 25.3],
                           [-3.3, -4.7, 25.3],
                           [0.5, 1.3, 29.1],
                           [0.5, -4.7, 29.1],
                           [-3.9, 1.3, 32.5],
                           [-3.9, -4.7, 32.5]],
                          [[-12.8, 1.3, 24.4],
                           [-12.8, -4.7, 24.4],
                           [-6.9, 1.3, 21.7],
                           [-6.9, -4.7, 21.7],
                           [-4.4, 1.3, 27.0],
                           [-4.4, -4.7, 27.0],
                           [-10., 1.3, 29.7],
                           [-10., -4.7, 29.7]
                           ]])