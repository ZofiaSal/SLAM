import streamlit as st
import numpy as np
from PIL import Image

intrinsicMatrix = np.matrix(
[[903.29304297,   0.,         647.28747544],
 [  0.,         904.78000567, 358.91564315],
 [  0.,           0.,           1.,        ]])

extrinsicMatrix =  [[1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]]

projectionMatrix = intrinsicMatrix.dot(extrinsicMatrix)

# Interactive Streamlit elements, like these sliders, return their value.
# This gives you an extremely simple interaction model.
positionX = st.sidebar.slider("Position X", -30, 30, 0, 1)
positionY = st.sidebar.slider("Position Y", -30, 30, 0, 1)
positionZ = st.sidebar.slider("Position Z", 10, 100, 30, 1)
uploadedImageFile = st.file_uploader("Image")
uploadedImage = Image.open(uploadedImageFile)

homogeneous3D = np.matrix([positionX, positionY, positionZ, 1]).T

homogeneous2D = projectionMatrix * homogeneous3D

point2D = homogeneous2D[:-1] / homogeneous2D[-1]
print(point2D)


# These two elements will be filled in later, so we create a placeholder
# for them using st.empty()
frame_text = st.sidebar.empty()
image = st.empty()
sizeX = 1280
sizeY = 720
N = np.zeros((sizeY, sizeX))

pictureX = int(point2D[0])
pictureY = int(point2D[1])
width = 10
try:
    print(uploadedImage)
except:
    Image.open('images_of_charuco_from_realsense/2023_03_04_16_59_39photo.jpg')

if (pictureX in range(width, sizeX)) and (pictureY in range(width, sizeY)):
    for pixelX in range(sizeX - pictureX - width, sizeX - pictureX):
        for pixelY in range(sizeY - pictureY - width, sizeY - pictureY):
            uploadedImage.putpixel((pixelX, pixelY), (255,0,0,0))
            N[(sizeY - pictureY - width):(sizeY - pictureY), (sizeX - pictureX - width):(sizeX - pictureX)] = 1

print(pictureX)
print(pictureY)


image.image(uploadedImage)
print(image)

# We clear elements by calling empty on them.
frame_text.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")