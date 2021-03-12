from src.yoloDetection import object_detection
from src.tracker import *

class CarSpeedEstimator:
    def __init__(self, video, start_line, end_line, length):
        self.cap = video
        self.Detection = object_detection()
        self.frame_counter = 0
        self.roi_param = [150, 50, 550, 450]
        self.first_line = start_line
        self.second_line = end_line

        #   Optical flow preparation
        _, frame = self.cap.read()
        old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.tracker = OpticalPointTracker(old_gray, self.first_line, self.second_line, length)

        #   Video output preparation
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        self.out = cv2.VideoWriter("Result.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                   30, (frame_width, frame_height))

    def run(self):
        while True:

            #   Frame preparation
            self.frame_counter = self.frame_counter + 1
            _, frame = self.cap.read()
            x, y, w, h = self.roi_param
            roi = frame[y: y + h, x: x + w]

            #   Object detection
            roi, boxes = self.Detection.detect_objects(roi, 0.6)

            #   Update tracker
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            boxes_ids, speed = self.tracker.update(boxes, gray_frame, self.roi_param)

            #   Draw Lines
            cv2.line(frame, self.first_line[0], self.first_line[1], (0, 0, 250), 2)
            cv2.line(frame, self.second_line[0], self.second_line[1], (0, 0, 250), 2)

            #   Name boxes
            for box_id in boxes_ids:
                x, y, px, py, id = box_id
                if speed[id] != 0:
                    text = str(speed[id])
                    cv2.putText(frame, text, (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 250), 2)
                cv2.circle(frame, (px, py), 3, (0, 255, 0), -1)

            #   Show and save frame
            self.out.write(frame)
            cv2.imshow("frame", roi)
            key = cv2.waitKey(1)
            print(self.frame_counter)
            if key == 27 or self.frame_counter > 1200:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Hotovo")
        return True