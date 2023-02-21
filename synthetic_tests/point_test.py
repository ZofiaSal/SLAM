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

    # Only rotating around the center of coordinate system. 
    def onlyRotationTest(self):
        self.__equalRotations([pi], [-pi], pt.Point(1,4,2))
        self.__equalRotations([pi,pi,pi], [3*pi], pt.Point(2,-5,3))
        self.__equalRotations([1,2,3], [3,2,1], pt.Point(-9,-3,3))

        # The point with the cetner and Y creates a triangle 45, 45, 90.
        point = pt.Point(1,1,4)
        point.changeOriginByRotationInXY(pi/4)
        assert( point == pt.Point(0,math.sqrt(2),4))

        # Lnegth of vector to the point should stay the same
        point1 = pt.Point(12,23,78)
        point2 = copy.copy(point1)
        for angle in [1,4,6,7,2,10,12]:
            point2.changeOriginByRotationInXY(angle)
            assert(point1.egualLength(point2))


    # Sum of rotations angles1 is equal to the sum of rotations angles2.
    def __equalRotations(self, angles1, angles2, pointStart):
        point1 = copy.copy(pointStart)
        point2 = copy.copy(pointStart)
    
        for angle in angles1:
            point1.changeOriginByRotationInXY(angle)

        for angle in angles2:
            point2.changeOriginByRotationInXY(angle)

        assert(point1 == point2)



    def onlyTranslationTest(self):
        translations = [[1,1], [-5,-7], [-3,7], [0,0]]
        for translation in translations:
            self.__onlyTranslationForCenterPoint(translation)

        # Both translations move the origin to [-7,-7] .
        translations1 = [[1,6],[-2,3],[-6,-2]]
        translations2 = [[-1,-1],[-6,8]]
        self.__OnlyTranslationDifferentPaths(pt.Point(0,0,0), translations1, translations2)
        self.__OnlyTranslationDifferentPaths(pt.Point(2,-1,6),translations1, translations2)
        
    def __OnlyTranslationDifferentPaths(self, pointStart, translations1, translations2):
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
    test = PointTest()
    test.run()

if __name__ == '__main__':
    main()
