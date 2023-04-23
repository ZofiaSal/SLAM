from cmath import pi

# Change depending on movement !!
ROTATION = - pi / 9   # in radians
XMOVEMENT = - 0.0427171547           # in meters
ZMOVEMENT = 0.0567852171           # in meters

MOVEMENTS = []
for i in range(21):
    movement = [XMOVEMENT, ZMOVEMENT, ROTATION]
    MOVEMENTS.append(movement)