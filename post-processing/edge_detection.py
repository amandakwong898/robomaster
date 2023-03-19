# importing the necessary libraries
import cv2
import numpy as np

"""
Referenced https://www.geeksforgeeks.org/python-process-images-of-a-video-using-opencv/.
Will add more features soon.
"""

# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('DJI_0001.MP4')

# Loop until the end of the video
while (cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()

	frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0,
						interpolation = cv2.INTER_CUBIC)

	# Display the resulting frame
	cv2.imshow('Frame', frame)

	# using cv2.Canny() for edge detection.
	edge_detect = cv2.Canny(frame, 100, 200)
	cv2.imshow('Edge detect', edge_detect)

	# define q as the exit button
	if cv2.waitKey(25) & 0xFF == ord('q'):
		break

# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()
