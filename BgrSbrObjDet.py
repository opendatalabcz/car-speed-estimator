import cv2
import numpy as np
from PointManager import manager
import time


kernel_dil = np.ones((20, 20), np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture("Data/cam_2.mp4")

_, frame = cap.read()
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

lk_params = dict(winSize = (15, 15), maxLevel = 4,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

point_selected = False
point = ()
old_points2 = manager()

def select_point(event, x, y, flags, params):
    global point, point_selected, old_points2
    if event == cv2.EVENT_LBUTTONDOWN:
        point = (x, y)
        point_selected = True
        old_points2.add_point(x, y)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_point)

while True:
    ret, frame = cap.read()
    time.sleep(1/60)
    fshape = frame.shape
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if ret == True:
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(fgmask, kernel_dil, iterations = 1)
        (contours, hierarchy) = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 3500):
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#                cv2.circle(frame, (x + int(w/2), y + int(h/2)), 5, (0, 255, 0), -1)

    if point_selected:
        new_points, status, error = cv2.calcOpticalFlowPyrLK(old_gray, gray_frame, old_points2.getAll(), None, **lk_params)
        old_gray = gray_frame.copy()
        position = 0
        for point in new_points:
            x, y = point.ravel()
            old_points2.rewrite(position,x,y)
            position = position + 1
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
