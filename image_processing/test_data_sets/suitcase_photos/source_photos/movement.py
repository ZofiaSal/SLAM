from cmath import pi

# Change depending on movement !!
ROTATION = - pi / 9   # in radians
XMOVEMENT = - 4.27171547           # in meters
ZMOVEMENT = 5.67852171           # in meters

MOVEMENTS = []
for i in range(18):
    movement = [XMOVEMENT, ZMOVEMENT, ROTATION]
    MOVEMENTS.append(movement)