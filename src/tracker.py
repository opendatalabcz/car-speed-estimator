import cv2
import numpy as np
from src import LPFinder as LPFinder
from src.speedMeasure import *
from src.vehicle import vehicle

class OpticalPointTracker:
    def __init__(self, gray, line1, line2, length):
        self.optical_points = {}
        self.vehicles = {}
        self.id_count = 0
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.old_gray = gray
        self.speedEst = SpeedMeasure(line1, line2, length)

    #   Find if points is outside of frame
    def point_outside(self, point, frame_params):
        ret = False
        x, y, w, h = frame_params
        x1, y1 = point
        if x < x1 < x + w and y < y1 < y + h:
            ret = True
        return ret

    #   Update tracker and get speed for each car
    def update(self, objects_rect, gray_frame, frame_param):
        objects_bbs_ids = []
        speed = {}

        #   If we already have points to follow
        if self.vehicles.items():

            #   Split id and points
            points = []
            ids = []
            for id, pt in self.optical_points.items():
                points.append(pt)
                ids.append(id)

            #   Calculate new position of points
            prepared_optical_points = np.array(points, dtype=np.float32)
            new_points, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                        prepared_optical_points, None, **self.lk_params)

            #   Match points and ids
            new_optical_points = {}
            for i in range(len(ids)):
                new_optical_points[ids[i]] = new_points[i]

            #   Remove points outside of frame
            self.optical_points = {}
            for id, point in new_optical_points.items():
                if self.point_outside(point, frame_param):
                    self.optical_points[id] = point
                    self.vehicles[id].update_point(point)
                else:
                    self.vehicles.pop(id, None)

            #   Get point speed
            speed = self.speedEst.measure_speed(self.optical_points)

        #   Find match rectangles and points
        for rect in objects_rect:
            x, y, w, h = rect

            # Find out if that object was detected already
            same_object_detected = False
            if self.vehicles.items():
                for _, car in self.vehicles.items():
                    pt = car.get_point()
                    if x < pt[0] < x + w and y < pt[1] < y + h:
                        car.update_rect(rect)
                        objects_bbs_ids.append(car.get_info())
                        same_object_detected = True
                        break

            # If new object is detected we assign the ID to that object
            if same_object_detected is False:
                tmp_vehicle = vehicle(rect, self.id_count)
                tmp_vehicle.create_points(gray_frame)
                self.vehicles[self.id_count] = tmp_vehicle
                self.optical_points[self.id_count] = tmp_vehicle.get_point()
                objects_bbs_ids.append(tmp_vehicle.get_info())
                speed[self.id_count] = 0
                self.id_count += 1

        #   Save frame for next step
        self.old_gray = gray_frame
        return objects_bbs_ids, speed
