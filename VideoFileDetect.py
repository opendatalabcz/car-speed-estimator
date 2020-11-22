from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
from PictureObjectDetection import object_detection

cap = cv2.VideoCapture("Data/TestCam.mp4")
detection = object_detection()
n = 0
while cap.isOpened():
    n = n + 1
    frame = cap.read()
    if n == 10:
        n = 0
        frame = detection.detect_objects(frame, 0.6, True)

        cv2.imshow("Frame", frame)
    print(n)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows
cap.release()