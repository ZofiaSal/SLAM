import streamlit as st
import numpy as np
from PIL import Image

INTRINSIC_MATRIX = np.matrix(
[[903.29304297,   0.,         647.28747544],
 [  0.,         904.78000567, 358.91564315],
 [  0.,           0.,           1.,        ]])

EXTRINSIC_MATRIX =  [[1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]]

# Width of the squared point
WIDTH = 8

if 'points' not in st.session_state:
    st.session_state['points'] = []


def putPixelOnPhoto( picX, picY, image):
    sizeX = image.width
    sizeY = image.height

    # Photo in pixels.
    N = np.zeros((sizeY, sizeX))

    if (picX in range(WIDTH, sizeX)) and (picY in range(WIDTH, sizeY)):
        for pixelX in range(sizeX - picX - WIDTH, sizeX - picX):
            for pixelY in range(sizeY - picY - WIDTH, sizeY - picY):
                image.putpixel((pixelX, pixelY), (255,0,0,0))
                N[(sizeY - picY - WIDTH):(sizeY - picY), (sizeX - picX - WIDTH):(sizeX - picX)] = 1

def addSaveButton():
    if st.button('Save the point'):
        if 'points' not in st.session_state:
            st.session_state['points'] = []
        st.session_state['points'].append((pictureX,pictureY))

        print(st.session_state['points'])


projectionMatrix = INTRINSIC_MATRIX.dot(EXTRINSIC_MATRIX)

# Interactive Streamlit elements, like these sliders, return their value.
# This gives you an extremely simple interaction model.
positionX = st.sidebar.slider("Position X", -30, 30, 0, 1)
positionY = st.sidebar.slider("Position Y", -30, 30, 0, 1)
positionZ = st.sidebar.slider("Position Z", 10, 100, 30, 1)

# Counting pixel coordinates of the point on the photo
homogeneous3D = np.matrix([positionX, positionY, positionZ, 1]).T
homogeneous2D = projectionMatrix * homogeneous3D
point2D = homogeneous2D[:-1] / homogeneous2D[-1]
print(point2D)
pictureX = int(point2D[0])
pictureY = int(point2D[1])

# Add the uploader of photos.
uploadedImageFile = st.file_uploader("Image")

# This element will be filled in later, so we create a placeholder
# for it using st.empty().
image = st.empty()

# Try getting a photo to show.
try:

    uploadedImage = Image.open(uploadedImageFile)

    putPixelOnPhoto(pictureX, pictureY, uploadedImage)

    
    for i,j in st.session_state['points']:
        putPixelOnPhoto(i, j, uploadedImage)

    image.image(uploadedImage)

    addSaveButton()

    if st.button('Clear all points'):
        st.session_state['points'] = []

except:
    print("No file uploaded or sth else")
