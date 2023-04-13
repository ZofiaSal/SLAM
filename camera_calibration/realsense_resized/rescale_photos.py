import cv2
import os

# Set the directories for input and output
input_dir = "./realsense"
output_dir = "./realsense_resized"

# Set the desired size for the images
new_size = (1280, 720)

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Get the full path of the input file
    input_path = os.path.join(input_dir, filename)

    # Load the image
    img = cv2.imread(input_path)

    # Resize the image
    resized_img = cv2.resize(img, new_size)

    # Get the full path of the output file
    output_path = os.path.join(output_dir, filename)

    # Save the resized image
    cv2.imwrite(output_path, resized_img)