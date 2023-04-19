from cmath import pi

# Change depending on movement !!
ROTATION = - pi / 6           # in radians
XMOVEMENT = - 0.0243833765112           # in meters
ZMOVEMENT = 0.091           # in meters

# 9.42101324173

MOVEMENTS = [[XMOVEMENT, ZMOVEMENT, ROTATION]]

# Usethis for circle movement
MOVEMENTS = []
for i in range(2):
    movement = [XMOVEMENT, ZMOVEMENT, ROTATION]
    MOVEMENTS.append(movement)