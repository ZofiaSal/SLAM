import numpy as np
import cv2

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

# The function will return the points that are seen by the camera.
def only_seen_points(points3D):
    result = []
    for i in range(len(points3D)):
        point3D = points3D[i]
        if point3D[2] > 0:
            point2d = cv2.projectPoints(point3D, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), cameraMatrix, distCoeffs)
            point2d = point2d[0].reshape(-1, 2)
            point2d = point2d.astype(int)
            if point2d[0][0] > 0 and point2d[0][0] < 1280 and point2d[0][1] > 0 and point2d[0][1] < 720:
                result.append(point3D)

    return np.array(result)
