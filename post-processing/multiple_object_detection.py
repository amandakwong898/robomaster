"""
multiple_object_detection.py:

This program implements centroid-based object tracking
and creates bounding boxes on distinct objects within
its view. A unique ID is assigned to each object being tracked.
"""

from tracker import EuclideanDistTracker
import cv2
import numpy as np

cap = cv2.VideoCapture('DJI_0001.MP4')  # REPLACE WITH PATH TO MP4
ret, frame1 = cap.read()
ret, frame2 = cap.read()

tracker = EuclideanDistTracker()

while cap.isOpened():
    ret, frame = cap.read()
    # this method is used to find the difference bw two frames
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    height, width = blur.shape
    print(height, width)

    thresh_value = cv2.getTrackbarPos('thresh', 'trackbar')
    _, threshold = cv2.threshold(blur, 23, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, (1, 1), iterations=1)
    contours, _, = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 300:
            continue
        detections.append([x, y, w, h])

    # return a list of bounding boxes with their corresponding IDs
    boxes_ids = tracker.update(detections)

    #  loop through this list and draw the bounding boxes and IDs on the frame
    for box_id in boxes_ids:
        x, y, w, h, identifier = box_id
        cv2.putText(frame1, str(identifier), (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    key = cv2.waitKey(30)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
