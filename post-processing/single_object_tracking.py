"""
single_object_tracking.py:

This program post-processes an MP4 file an applies a Gaussian blur
to the video to remove detail and noise. It also uses Otsu's thresholding
method to create a binary image, and finds the largest contour in the
binary image to draw the bounding box.
"""

# importing the necessary libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('DJI_0001.MP4')

# Total number of frames in video
frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(f'Frame count: {frames}')
# Video height and width
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print(f'Height: {height}\nWidth: {width}')
# Get frames per second
fps = cap.get(cv2.CAP_PROP_FPS)
print(f'FPS: {fps:0.2f}')

# Pulling images from video
ret, img = cap.read()
print(f'Returned {ret} and img of shape {img.shape}')

# Loop until the end of the video
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (540, 380), fx=0, fy=0,
                       interpolation=cv2.INTER_CUBIC)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    _, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the binary image
    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the bounding box coordinates of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Draw the bounding box on the frame
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Use cv2.Gaussianblur() method to blur the video
    # (5, 5) is the kernel size for blurring.
    gaussianblur = cv2.GaussianBlur(frame, (5, 5), 0)
    img = cv2.imshow('gblur', gaussianblur)

    # define q as the exit button
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# release the video capture object
cap.release()

# Closes all the windows currently opened.
cv2.destroyAllWindows()
