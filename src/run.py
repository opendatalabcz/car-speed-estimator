import cv2
from src.carSpeedEstimator import *

cap = cv2.VideoCapture("Data/my_traffic.mp4")
test = CarSpeedEstimator(cap)
test.run()
