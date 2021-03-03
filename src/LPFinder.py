import cv2
import imutils
import numpy as np

def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

def FindLP(img):
    squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    light = cv2.morphologyEx(img, cv2.MORPH_CLOSE, squareKern)
    light = cv2.threshold(light, 0, 255,
                          cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    keypoints = cv2.findContours(light.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 3, True)
        if len(approx) == 4:
            location = approx
            break

    x = 0
    y = 0

    if location is not None:
        for point in location:
            x1, y1 = point.ravel()
            x = x + x1
            y = y + y1
        x = int(x/4)
        y = int(y/4)
    else:
        h, w = img.shape
        y = h // 2
        x = w // 2

    return x, y
