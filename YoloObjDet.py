import cv2
from PictureObjectDetection import object_detection
from tracker import *
import LPFinder as LPFinder
import numpy as np

class speed_meter:
    def __init__(self, frame_in):
        self.cap = frame_in
        self.Detection = object_detection()
        self.tracker = EuclideanDistTracker()
        self.frame_counter = 0
        self.optical_points = []
        self.roi_param = [100, 150, 650, 450]

        # Optical flow preparation
        _, frame = cap.read()
        self.old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.tracker2 = OpticalPointTracker(self.old_gray)
        self.lk_params = dict(winSize=(15, 15),
                         maxLevel=2,
                         criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # Video output preparation
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        self.out = cv2.VideoWriter("outpyYolo.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                   30, (frame_width, frame_height))

    def add_points(self, boxes, frame):
        for box in boxes:
            if self.points_check(box, self.optical_points):
                continue

            x, y, w, h = box
            if x < 0:
                x = 0
            if y < 0:
                y = 0

            object_img = frame[y:y + h, x:x + w]
            px, py = LPFinder.FindLP2(object_img)
            if px == 0:
                px = w // 2
                py = h // 2
            self.optical_points.append([x + self.roi_param[0] + px, y + self.roi_param[1] + py])

    def points_check(self, box, points):
        ret = False
        x, y, w, h = box
        x = x + self.roi_param[0]
        y = y + self.roi_param[1]
        for point in points:
            x1, y1 = point
            if x < x1 < x + w and y < y1 < y + h:
                ret = True
                break
        return ret

    def caluculate_points(self, frame, gray_frame):
        prepared_optical_points = np.array(self.optical_points, dtype=np.float32)
        new_points, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                    prepared_optical_points, None, **self.lk_params)
        self.optical_points = []
        roi_x, roi_y, roi_w, roi_h = self.roi_param

        #         Check if existing points are still in frame
        for point in new_points:
            x, y = point.ravel()
            if x > roi_x + roi_w or y > roi_y + roi_h or x < roi_x or y < roi_y:
                continue
            self.optical_points.append([x, y])
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    def run(self):
        while True:
            #     Frame preparation
            self.frame_counter = self.frame_counter + 1
            _, frame = self.cap.read()
            x, y, w, h = self.roi_param
            roi = frame[y: y + h, x: x + w]

            #     Object detection
            roi, boxes = self.Detection.detect_objects(roi, 0.8, False)

            #     Update tracker
            boxes_ids, new_boxes = self.tracker.update(boxes)

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.optical_points:
                self.caluculate_points(frame, gray_frame)

            #     Add new points
            self.add_points(new_boxes, frame)

            #     Save frame for next calculation
            self.old_gray = gray_frame.copy()

            #     Name boxes
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)

            self.out.write(frame)
#            cv2.imshow("frame", roi)
            key = cv2.waitKey(1)
            print(self.frame_counter)
            if key == 27 or self.frame_counter > 1200:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Hotovo")

    def run2(self):
        while True:

            #     Frame preparation
            self.frame_counter = self.frame_counter + 1
            _, frame = self.cap.read()
            x, y, w, h = self.roi_param
            roi = frame[y: y + h, x: x + w]

            #     Object detection
            roi, boxes = self.Detection.detect_objects(roi, 0.6, False)

            #     Update tracker
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            boxes_ids = self.tracker2.update(boxes, gray_frame, self.roi_param)

            #     Name boxes
            for box_id in boxes_ids:
                x, y, px, py, id = box_id
                cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
                cv2.circle(frame, (px, py), 3, (0, 255, 0), -1)

            self.out.write(frame)
#            cv2.imshow("frame", roi)
            key = cv2.waitKey(1)
            print(self.frame_counter)
            if key == 27 or self.frame_counter > 1200:
                break

        self.cap.release()
        cv2.destroyAllWindows()
        print("Hotovo")


cap = cv2.VideoCapture("Data/my_traffic.mp4")
test = speed_meter(cap)
test.run2()