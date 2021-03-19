from src.yoloDetection import object_detection
from src.tracker import *

class CarSpeedEstimator:
    def __init__(self, video, start_line, end_line, length):
        self.cap = video
        self.Detection = object_detection()
        self.frame_counter = 0
        self.first_line = start_line
        self.second_line = end_line

        #   Optical flow preparation
        _, frame = self.cap.read()
        old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #   Video output preparation
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        self.out = cv2.VideoWriter("Result.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                   30, (frame_width, frame_height))
        self.frame_param = [0, 0, frame_width, frame_height]
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.tracker = OpticalPointTracker(old_gray, self.first_line, self.second_line, length, self.fps)

    def run(self):
        while True:
            #   Frame preparation
            self.frame_counter = self.frame_counter + 1
            _, frame = self.cap.read()
            #   Object detection
            frame, boxes = self.Detection.detect_objects(frame, 0.6)

            #   Update tracker
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            boxes_ids, speed = self.tracker.update(boxes, gray_frame, self.frame_param)

            #   Draw Lines
            cv2.line(frame, self.first_line[0], self.first_line[1], (0, 0, 250), 2)
            cv2.line(frame, self.second_line[0], self.second_line[1], (0, 0, 250), 2)

            #   Create boxes
            for box in boxes:
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 250), 2)

            #   Name boxes
            for box_id in boxes_ids:
                x, y, px, py, id = box_id
                if speed[id] != 0:
                    text = str(speed[id])
                    cv2.putText(frame, text, (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 250), 2)
                cv2.circle(frame, (px, py), 3, (0, 255, 0), -1)

            #   Show and save frame
            self.out.write(frame)
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1)
            print(self.frame_counter)
            if key == 27 or self.frame_counter > self.fps*50:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Hotovo")
        return True
