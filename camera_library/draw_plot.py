import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('./')
import photos_from_realsense.description as desc


A = desc.points2D_im1

# Split the matrix into x and y coordinates
x = []
y = []
for point in A:
    x.append(point[1][0])
    y.append(point[1][1])

x = [45.0, 134.0, 223.0, 312.0, 401.0, 490.0, 579.0, 668.0, 
     118.0, 207.0, 296.0, 385.0, 474.0, 563.0, 652.0, 103.0, 
     191.0, 280.0, 369.0, 458.0, 547.0, 636.0, 87.0, 176.0, 
     264.0, 353.0, 442.0, 531.0, 620.0, 71.0, 160.0, 249.0, 
     338.0, 426.0, 515.0, 604.0, 55.0, 144.0, 233.0, 322.0, 
     411.0, 499.0, 588.0]

y = [536.0, 517.0, 498.0, 479.0, 460.0, 441.0, 423.0, 404.0, 
     441.0, 422.0, 403.0, 385.0, 366.0, 347.0, 328.0, 365.0, 
     346.0, 328.0, 309.0, 290.0, 271.0, 252.0, 289.0, 271.0, 
     252.0, 233.0, 214.0, 195.0, 177.0, 214.0, 195.0, 176.0, 
     157.0, 138.0, 120.0, 101.0, 138.0, 119.0, 100.0, 81.0, 
     63.0, 44.0, 25.0]

img = plt.imread("photos_from_realsense/undist1.jpg")
fig, ax = plt.subplots()
ax.imshow(img)

# Plot the points
plt.plot(x, y, 'r.', markersize=2)
plt.xlim(0, 1280)
plt.ylim(0, 720)
plt.gca().invert_yaxis()

plt.savefig('photos_from_realsense/plot1.jpg', dpi=600)