from src.yoloDetection import object_detection
from src.tracker import *
from src.speedMeasure import *

#   Starting class.
class CarSpeedEstimator:
    def __init__(self, video, start_line, end_line, length):
        #   Variable setup
        self.cap = video
        self.detection = object_detection()
        self.frame_counter = 1
        self.first_line = start_line
        self.second_line = end_line
        self.n_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT);

        #   Video output preparation
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.output_video = cv2.VideoWriter("Result.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                            fps, (frame_width, frame_height))

        #   Tracker preparation
        _, frame = self.cap.read()
        old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.frame_param = [0, 0, frame_width, frame_height]
        speedEst = SpeedMeasure(self.first_line, self.second_line, length, fps)
        self.tracker = OpticalPointTracker(old_gray, self.frame_param, speedEst)

    def remove_border_boxes(self, boxes):
        ret_boxes = []
        for rect in boxes:
            stay = False
            x, y, w, h = rect
            if 10 < x and 10 < y and x + w < self.frame_param[2] - 10 and y + h < self.frame_param[3] - 10:
                stay = True
            if stay:
                ret_boxes.append(rect)
        return ret_boxes

    def run(self):
        while True:
            #   Get new frame
            self.frame_counter = self.frame_counter + 1
            _, frame = self.cap.read()

            #   Detect objects in frame
            frame, boxes = self.detection.detect_objects(frame, 0.5)
            boxes = self.remove_border_boxes(boxes)

            #   Update tracker
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            boxes_ids, speed = self.tracker.update(boxes, gray_frame)

            #   Draw Lines of measured area
            cv2.line(frame, self.first_line[0], self.first_line[1], (0, 0, 250), 2)
            cv2.line(frame, self.second_line[0], self.second_line[1], (0, 0, 250), 2)

            #   Draw object bounding boxes
            for box in boxes:
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 2)

            #   Show vehicle speed
            for box_id in boxes_ids:
                x, y, px, py, id = box_id
                text = str(id)
                if speed[id] != 0:
                    text += ": "
                    text += str(speed[id])
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 250), 2)

            #   Show and save frame
            self.output_video.write(frame)
            cv2.imshow("frame", frame)
            key = cv2.waitKey(1)
            print(self.frame_counter)
            if key == 27 or self.frame_counter == self.n_frames:
                break
        #   Cleaning
        self.cap.release()
        self.tracker.create_csv()
        cv2.destroyAllWindows()
        print("Done")
