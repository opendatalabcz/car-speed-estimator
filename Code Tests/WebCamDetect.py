from imutils.video import VideoStream
from imutils.video import FPS
from queue import Queue
import threading
import imutils
import time
import cv2
from Data.PictureObjectDetection import object_detection

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
frames = []
queue = Queue()
end_frames = Queue()
detection_continue = True

def detections():
    detection = object_detection()
    while not queue.empty():
        print(queue.qsize())
        frame = queue.get()
        end_frames.put(detection.detect_objects(frame, 0.6, False))

#with concurrent.futures.ThreadPoolExecutor() as executor:
#    f1 = executor.submit(detections, frame)

t1 = threading.Thread(target=detections)
t2 = threading.Thread(target=detections)
t3 = threading.Thread(target=detections)
test = 0

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    queue.put(frame)

    if test == 2:
        t3.start()
        test = 3
    if test == 1:
        t2.start()
        test = 2
    if test == 0:
        t1.start()
        test = 1


    time.sleep(0.2)
    if not end_frames.empty():
        cv2.imshow("Frame", end_frames.get())
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        detection_continue = False
        break

    fps.update()


t1.join()
t2.join()
t3.join()
fps.stop()
cv2.destroyAllWindows
vs.stop()