import cv2
import numpy as np
from PointManager import manager
from PictureObjectDetection import object_detection
from tracker import *
import time


kernel_dil = np.ones((5, 5), np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
cap = cv2.VideoCapture("Data/cam_2.mp4")
detection = object_detection()

_, frame = cap.read()
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
out = cv2.VideoWriter("outpyBackground.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width, frame_height))
tracker = EuclideanDistTracker()

lk_params = dict(winSize = (15, 15), maxLevel = 4,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

fshape = frame.shape
old_points = manager(fshape)

def select_point(event, x, y, flags, params):
    global old_points
    if event == cv2.EVENT_LBUTTONDOWN:
        old_points.add_point(x, y)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)

while True:
    ret, frame = cap.read()
    time.sleep(1/60)
    fshape = frame.shape
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    roi = frame[150: 600,100: 750]

    if ret == True:
        fgmask = fgbg.apply(roi)
        _, fgmask = cv2.threshold(fgmask, 100, 255, cv2.THRESH_BINARY)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(fgmask, kernel_dil, iterations = 1)
        erosion = cv2.erode(fgmask,kernel_dil,iterations = 1)
#        dilation = cv2.dilate(erosion, kernel_dil, iterations=1)
#        cv2.imshow("dilitation", fgmask)
        (contours, hierarchy) = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detection = []
#        (contours, hierarchy) = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 2500):
                x, y, w, h = cv2.boundingRect(contour)
                detection.append([x, y , w, h])
                img = cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                old_points.add_point(x + int(w/2), y + int(h/2))
#                cv2.circle(frame, (x + int(w/2), y + int(h/2)), 5, (0, 255, 0), -1)

    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y -15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
#    print(boxes_ids)

#    roi = detection.detect_objects(roi, 0.6, False)
#    if old_points.point_selected():
#        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points.getAll(), None, **lk_params)
#        old_gray = gray_frame.copy()
#        position = 0
#        old_points.rewrite(new_points)
#        for point in new_points:
#            x, y = point.ravel()
#            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    cv2.imshow("fgmask", fgmask)
    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    out.write(frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
