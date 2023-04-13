from cmath import pi
import math
import copy
import sys
sys.path.append('../')
import point as pt

class PointTest:
    def run(self):
        self.onlyTranslationTest()
        print("passed onlyTranslationTest")
        self.onlyRotationTest()
        print("passed onlyRotationTest")
        self.fullMovementTest()
        print ("passed fullMovementTest")
        self.fullMovementSimpleTest()
        print ("passed fullMovementSimpleTest")

    def fullMovementTest(self):
        # The point with the center and Y creates a triangle 45, 45, 90.
        point = pt.Point(1,1,0)
        point.changeOriginByMovementInXY([0,0,-pi/4])
        point.changeOriginByMovementInXY([0,math.sqrt(2),0])
        assert(point == pt.Point(0,0,0))

        point = pt.Point(1,1,5)
        point.changeOriginByMovementInXY([2,0,pi/2])
        assert(point == pt.Point(1,1,5))

    # Only rotating around the center of coordinate system. 
    def onlyRotationTest(self):
        self.__equalRotations([pi], [-pi], pt.Point(1,4,2))
        self.__equalRotations([pi,pi,pi], [3*pi], pt.Point(2,-5,3))
        self.__equalRotations([1,2,3], [3,2,1], pt.Point(-9,-3,3))

        # The point with the cetner and Y creates a triangle 45, 45, 90.
        point = pt.Point(1,1,4)
        point.changeOriginByRotationInXY(-pi/4)
        assert( point == pt.Point(0,math.sqrt(2),4))

        # Length of a vector should stay the same after rotations.
        point1 = pt.Point(12,23,78)
        point2 = copy.copy(point1)
        for angle in [1,4,6,7,2,10,12]:
            point2.changeOriginByRotationInXY(-angle)
            assert(point1.equalLength(point2))

    # Sum of rotations angles1 is equal to the sum of rotations angles2.
    def __equalRotations(self, angles1, angles2, pointStart):
        point1 = copy.copy(pointStart)
        point2 = copy.copy(pointStart)
    
        for angle in angles1:
            point1.changeOriginByRotationInXY(angle)

        for angle in angles2:
            point2.changeOriginByRotationInXY(angle)

        assert(point1 == point2)

    def fullMovementSimpleTest(self):
        point = pt.Point(0, 1, 0)
        point.changeOriginByMovementInXY([0, 0, -pi/2])
        assert(point == pt.Point(-1, 0, 0))

        point = pt.Point(1, 1, 0)
        point.changeOriginByMovementInXY([1, 0, pi/2])
        assert(point == pt.Point(1, 0, 0))

        point = pt.Point(1, 1, 0)
        point.changeOriginByMovementInXY([1, 0, -pi/2])
        assert(point == pt.Point(-1, 0, 0))
        
        point = pt.Point(1, 1, 0)
        point.changeOriginByMovementInXY([0, 1, -pi/2])
        assert(point == pt.Point(0, 1, 0))

        point = pt.Point(1, 1, 0)
        point.changeOriginByMovementInXY([0, 2, -pi/2])
        assert(point == pt.Point(1, 1, 0))

    def onlyTranslationTest(self):
        translations = [[1,1], [-5,-7], [-3,7], [0,0]]
        for translation in translations:
            self.__onlyTranslationForCenterPoint(translation)

        # Both translations move the origin to [-7,-7] .
        translations1 = [[1,6],[-2,3],[-6,-2]]
        translations2 = [[-1,-1],[-6,8]]
        self.__onlyTranslationDifferentPaths(pt.Point(0,0,0), translations1, translations2)
        self.__onlyTranslationDifferentPaths(pt.Point(2,-1,6),translations1, translations2)
        
    def __onlyTranslationDifferentPaths(self, pointStart, translations1, translations2):
        point1 = copy.copy(pointStart)
        point2 = copy.copy(pointStart)
        for translation in translations1:
            point1.changeOriginByTranslation(translation[0], translation[1])
        for translation in translations2:
            point2.changeOriginByTranslation(translation[0], translation[1])
        assert(point1 == point2)
       
    def __onlyTranslationForCenterPoint(self, translation):
        point = pt.Point(0,0,0)
        point.changeOriginByTranslation(translation[0], translation[1])
        assert(point.x == -translation[0])
        assert(point.y == -translation[1])

def main():
    PointTest().run()

if __name__ == '__main__':
    main()
