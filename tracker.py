import math
import cv2
import numpy as np
import LPFinder as LPFinder


class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        self.optical_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []
        new_objects_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 40:
                    self.center_points[id] = (cx, cy)
                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                new_objects_ids.append([x, y, w, h])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        new_optical_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids, new_objects_ids

class OpticalPointTracker:
    def __init__(self, gray):
        self.optical_points = {}
        self.id_count = 0
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.old_gray = gray

    def point_outside(self, point, roi_params):
        ret = False
        x, y, w, h = roi_params
        x1, y1 = point
        if x < x1 < x + w and y < y1 < y + h:
            ret = True
        return ret

    def update(self, objects_rect, gray_frame, roi_param):
#               Calculate new points
        points = []
        ids = []
        if self.optical_points.items():
            for id, pt in self.optical_points.items():
                points.append(pt)
                ids.append(id)
            prepared_optical_points = np.array(points, dtype=np.float32)
            new_points, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                        prepared_optical_points, None, **self.lk_params)
#               Match points and ids
            new_optical_points = {}
            for i in range(len(ids)):
                new_optical_points[ids[i]] = new_points[i]

            self.optical_points = {}
#                   Filter points outside of region of interest
            for id, point in new_optical_points.items():
                if self.point_outside(point, roi_param):
                    self.optical_points[id] = point

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
                self.id_count += 1

        self.old_gray = gray_frame
        return objects_bbs_ids




