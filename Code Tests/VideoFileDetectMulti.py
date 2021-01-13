import cv2
from Data.PictureObjectDetection import object_detection
from multiprocessing import Process, Queue

def detections(qIn,qOut):
    detection = object_detection()
    while not qIn.empty():
        frame = qIn.get()[1]
        qOut.put(detection.detect_objects(frame, 0.6, False))
        print("hotovo")

cap = cv2.VideoCapture("Data/TestCam.mp4")
detection = object_detection()
n = 0
s = 0
qIn = Queue()
qOut = Queue()

p1 = Process(target=detections, args=(qIn,qOut))
p2 = Process(target=detections, args=(qIn,qOut))

while cap.isOpened():
    n = n + 1
    frame = cap.read()
    frame = frame[1]

    if n == 10:
        n = 0
        qIn.put(frame)
        if s == 1:
            p2.start()
            s = 2
        if s == 0:
            p1.start()
            s = 1

    if not qOut.empty():
        cv2.imshow("Frame", qOut.get()[1])

    print(n)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows
cap.release()