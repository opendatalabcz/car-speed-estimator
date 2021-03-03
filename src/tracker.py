import cv2
import numpy as np
from src import LPFinder as LPFinder
from src.SpeedMeter import *

class OpticalPointTracker:
    def __init__(self, gray, line1, line2):
        self.optical_points = {}
        self.id_count = 0
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.old_gray = gray
        y1 = line1[0][1]
        y2 = line2[0][1]
        self.speedEst = SpeedEstimator(y1, y2)

    def point_outside(self, point, roi_params):
        ret = False
        x, y, w, h = roi_params
        x1, y1 = point
        if x < x1 < x + w and y < y1 < y + h:
            ret = True
        return ret

    def update(self, objects_rect, gray_frame, roi_param):
        # Calculate new points
        points = []
        ids = []
        speed = {}
        if self.optical_points.items():
            for id, pt in self.optical_points.items():
                points.append(pt)
                ids.append(id)
            prepared_optical_points = np.array(points, dtype=np.float32)
            new_points, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                        prepared_optical_points, None, **self.lk_params)
            # Match points and ids
            new_optical_points = {}
            for i in range(len(ids)):
                new_optical_points[ids[i]] = new_points[i]
            self.optical_points = {}
            # Filter points outside of region of interest
            for id, point in new_optical_points.items():
                if self.point_outside(point, roi_param):
                    self.optical_points[id] = point
            speed = self.speedEst.estimate_speed(self.optical_points)

        objects_bbs_ids = []
        for rect in objects_rect:
            x, y, w, h = rect
            x = x + roi_param[0]
            y = y + roi_param[1]

            # Find out if that object was detected already
            same_object_detected = False
            if self.optical_points.items():
                for id, pt in self.optical_points.items():
                    if x < pt[0] < x + w and y < pt[1] < y + h:
                        objects_bbs_ids.append([x, y, pt[0], pt[1], id])
                        same_object_detected = True
                        break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                object_img = gray_frame[y:y + h, x:x + w]
                px, py = LPFinder.FindLP3(object_img)
                self.optical_points[self.id_count] = ([x + px, y + py])
                objects_bbs_ids.append([x, y, x + px, y + py, self.id_count])
                speed[self.id_count] = 0
                self.id_count += 1

        self.old_gray = gray_frame
        return objects_bbs_ids, speed