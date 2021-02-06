import cv2
import numpy as np
from PointManager import manager
from PictureObjectDetection import object_detection
from tracker import *
import time


cap = cv2.VideoCapture("Data/cam_2.mp4")
YoloDetection = object_detection()
_, frame = cap.read()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter("outpyYolo2.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width, frame_height))
tracker = EuclideanDistTracker()
frame_counter = 0

while True:
    frame_counter = frame_counter + 1
    ret, frame = cap.read()
    time.sleep(1/30)
    roi = frame[150: 600,100: 750]
    roi, boxes = YoloDetection.detect_objects(roi, 0.8, False)

    boxes_ids = tracker.update(boxes)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y -15), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
#    print(boxes_ids)

#    cv2.imshow("Frame", frame)
    out.write(frame)
    key = cv2.waitKey(1)
    print(frame_counter)
    if key == 27 or frame_counter > 600:
        break

cap.release()
cv2.destroyAllWindows()
print("Hotovo")
