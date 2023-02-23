import numpy as np
from cmath import pi
import math
import copy
import cv2
import sys
sys.path.append('../')
import image_processing as imgpr
import point as pt

class calculatePoints3DTest:
    def run(self):
        self.simpleTest()
        print("Passed simpleTest")
    
    def simpleTest(self):
        exampleIntrinsic =np.matrix([[542.517, 0.0, 239.5],[0, 542.517, 319.4],[0, 0, 1]])
        
        movement = [3, 2, 0]
        pointsBefore = np.array([[239.5, 319.5]])
        pointsAfter = np.array([[0, 319.5]])
        result = imgpr.calculatePoints3DSECOND( pointsBefore, pointsAfter, movement, exampleIntrinsic)
        print(cv2.convertPointsFromHomogeneous(result.T))


class getExtrinsicTest:
    def run(self):
        self.simpleTestMovementToThePoint()
        print("Passed simpleTestMovementToThePoint")
        self.testWithPointImpl()
        print("Passed testWithPointImpl")
    
    def simpleTestMovementToThePoint(self):
        pointBefore = np.matrix([1, 1, 1, 1]).T 
        
        movement1 = [1, 1, 0]      
        extrinsic1 = imgpr.getExtrinsic(movement1)
        pointAfter1 = pt.Point.fromNumpyMatrixHomogeneous((extrinsic1 @ pointBefore).T)
        assert(pointAfter1 == pt.Point.fromNumpyMatrixHomogeneous(np.matrix([0, 0, 1, 1])))
        
        # The rotation doesn't change anything since we moved to the coordinates of the point.
        movement2 = [1, 1, 3] 
        extrinsic2 = imgpr.getExtrinsic(movement2)
        pointAfter2 = pt.Point.fromNumpyMatrixHomogeneous((extrinsic2 @ pointBefore).T)
        assert(pointAfter2 == pt.Point.fromNumpyMatrixHomogeneous(np.matrix([0, 0, 1, 1])))

    def testWithPointImpl(self):
        # TODO: Add more tests?
        pointBefore = np.matrix([1, 1, 1, 1])
        point = pt.Point.fromNumpyMatrixHomogeneous(pointBefore)
        movement = [1, 5, 7]
        extrinsic = imgpr.getExtrinsic(movement)
        pointAfter = pt.Point.fromNumpyMatrixHomogeneous((extrinsic @ pointBefore.T).T)
        point.changeOriginByMovementInXY(movement)
        assert(pointAfter == point)



def main():
    calculatePoints3DTest().run()
    getExtrinsicTest().run()
    

if __name__ == '__main__':
    main()