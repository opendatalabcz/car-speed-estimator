import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture("Data/cam_2_rain.mp4")
backSub = cv2.createBackgroundSubtractorMOG2()

_, f = cap.read()

background = cap.read()[1]
scene_counter = 1

avg = np.float32(f)


while cap.isOpened():
    frame = cap.read()[1]
    scene_counter = scene_counter + 1

    background = (background + frame)/2
    cv2.imshow('Real Frame', frame)

#    cv2.accumulateWeighted(frame,avg,0.02)
#    res2 = cv2.convertScaleAbs(avg)

    fgMask = backSub.apply(frame)

    cv2.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    cv2.putText(frame, str(cap.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    backSub.getBackgroundImage(frame)

    minusArray = np.stack((fgMask, fgMask, fgMask))
    minusArray = np.transpose(minusArray, (1, 2, 0))

#   frame = frame - minusArray

    cv2.imshow('Background', frame)
#    cv2.imshow('FG Mask', fgMask)
#    cv2.imshow('avg', background)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows
cap.release()