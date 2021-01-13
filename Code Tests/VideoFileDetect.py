import cv2
from Data.PictureObjectDetection import object_detection

cap = cv2.VideoCapture("Data/TestCam.mp4")
detection = object_detection()
n = 0

while cap.isOpened():
    n = n + 1
    frame = cap.read()
    frame = frame[1]
    if n == 10:
        n = 0
        frame = detection.detect_objects(frame, 0.8, True)
        cv2.imshow("Frame", frame)
    print(n)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows
cap.release()