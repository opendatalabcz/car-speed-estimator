import time
import cv2
from src.PictureObjectDetection import object_detection

time.sleep(2.0)
detection = object_detection()

img = cv2.imread("../../Data/autobok10.jpg")
height, width, channels = img.shape
img = cv2.resize(img,(int(width/2),int(height/2)))

img = detection.detect_objects(img, 0.6, True)
print(img)
cv2.imshow("Frame", img)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
            break


cv2.destroyAllWindows