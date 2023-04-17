from cmath import pi

# Change depending on movement !!
ROTATION = pi / 8   # in radians
XMOVEMENT = 0.009           # in meters
ZMOVEMENT = 0.046           # in meters

MOVEMENTS = []
for i in range(16):
    movement = [XMOVEMENT, ZMOVEMENT, ROTATION]
    MOVEMENTS.append(movement)