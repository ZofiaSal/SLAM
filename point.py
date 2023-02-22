import numpy as np
import math
import cv2

 # Otherwise tests with unreal numbers won't work.
def equalWithRound(x, y):
    return round(x, 10) ==  round(y, 10)

class Point:

    # Create a new Point instance.
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z 
    
    def fromArray(coords):
        return Point( coords[0], coords[1], coords[2])

    def fromNumpyMatrixHomogeneous(pointH):
        point = cv2.convertPointsFromHomogeneous(pointH)[0][0]
        return Point.fromArray(point)


    # For tests.
    def __eq__(self, other):
        return equalWithRound(self.x, other.x) and equalWithRound(self.y, other.y) and equalWithRound(self.z, other.z)

    def __copy__(self):
        return Point(self.x, self.y, self.z)

    def __str__(self):
        return "( " + str(self.x) + ", " + str(self.y) + ", " + str(self.z)+ " )"

    def egualLength(self, other):
        return equalWithRound(self.__length(), other.__length())

    def __length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def toArray(self):
        return [self.x, self.y, self.z]

    # The center of coordinate system moves to the point [xMovement, yMovement, zMovement] .
    def changeOriginByTranslation(self, xMovement, yMovement, zMovement = 0):
        self.x = self.x - xMovement
        self.y = self.y - yMovement 
        self.z = self.z - zMovement

    # The center of coordinate system rotates clockwise (in XY plane) with an angle rotation (in radians).
    # Source: https://en.wikipedia.org/wiki/Rotation_of_axes
    def changeOriginByRotationInXY(self, rotation):
        x0 = self.x
        y0 = self.y
        self.x =  np.cos(rotation) * x0 - np.sin(rotation) * y0
        self.y =  np.sin(rotation) * x0 + np.cos(rotation) * y0
          
    # movement = [xMovement, yMovement, rotationXY(clockwise in radians)].
    def changeOriginByMovementInXY(self, movement):
        # First happens the translation and then the rotation so that rotation wouldn't change the coordinate system.
        self.changeOriginByTranslation(movement[0], movement[1])
        self.changeOriginByRotationInXY(movement[2])

    

