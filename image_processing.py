import numpy as np
import cv2
intrinsic = np.matrix([[1.09939263e+03, 0.00000000e+00, 2.82665849e+02],
    [0.00000000e+00, 1.08260264e+03, 1.81292903e+02],
    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

distortion = np.matrix([[ 2.33589358e+00, -6.07874111e+01, -2.29399415e-02,  8.79756112e-02, -1.45708167e-01]])

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# distance - the change from where picture 1 was taken to where picture 2 was taken [x,y,alpha]
def calculatePoints3D(points1, points2, distance):
    #calculate extrinsic matrix
    extrinsic1 = np.zeros((3,4))
    extrinsic1 = np.zeros((3,4))



    cv2.triangulatePoints()

    

def main():
    calculatePoints3D("hahaha", "elo", "xd")

if __name__ == '__main__':
    main()