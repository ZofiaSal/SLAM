from gettext import translation
import numpy as np
import cv2
intrinsic = np.matrix([[1.09939263e+03, 0.00000000e+00, 2.82665849e+02],
    [0.00000000e+00, 1.08260264e+03, 1.81292903e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distortion = np.matrix([[ 2.33589358e+00, -6.07874111e+01, -2.29399415e-02,  8.79756112e-02, -1.45708167e-01]])


def getRotationsInXY(angle):
    Rz = np.zeros(shape = (3, 3))
    Rz[0, 0] = np.cos(angle)
    Rz[0, 1] = -np.sin(angle)
    Rz[1, 0] = np.sin(angle)
    Rz[1, 1] = np.cos(angle)
    Rz[2, 2] = 1
    
    return Rz

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# distance - the change from where picture 1 was taken to where picture 2 was taken [x,y,alpha] where a lpha is rotation in XY
def calculatePoints3D(points1, points2, distance):
    
    #calculate extrinsic matrix
    rotation1 = np.identity(4)
    rotation1[:3, :3] = getRotationsInXY(-distance[2]) # with minus ?
    rotation2 = np.identity(4)

    translation1 = np.identity(4)
    translation1[:2, 3] = distance[:2]
    translation2 = np.identity(4)

    extrinsic1 = np.linalg.inv(rotation1 @ translation1)
    extrinsic2 = np.linalg.inv(rotation2 @ translation2)

    # remove last row of Extrinsic -> (3,4)
    extrinsic1 = extrinsic1[:-1, :]
    extrinsic2 = extrinsic2[:-1, :]

    projectionMatrix1 = intrinsic @ extrinsic1
    projectionMatrix2 = intrinsic @ extrinsic2


    return cv2.triangulatePoints(projectionMatrix1,projectionMatrix2, points1, points2)

    

def main():
    calculatePoints3D("hahaha", "elo", "xd")

if __name__ == '__main__':
    main()