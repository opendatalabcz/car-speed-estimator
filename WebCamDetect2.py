from imutils.video import VideoStream
from imutils.video import FPS
from queue import Queue
import threading
import concurrent.futures
import numpy as np
import argparse
import imutils
import time
import cv2
from PictureObjectDetection import object_detection

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
detection = object_detection()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = detection.detect_objects(frame, 0.6, False)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()


fps.stop()
cv2.destroyAllWindows
vs.stop()