import cv2
import numpy as np
from src import LPFinder as LPFinder
from src.speedMeasure import *
from src.vehicle import vehicle

class OpticalPointTracker:
    def __init__(self, gray, line1, line2, length, fps):
        self.vehicles = {}
        self.id_count = 0
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.old_gray = gray
        self.speedEst = SpeedMeasure(line1, line2, length, fps)

    #   Find if points is outside of frame
    def point_outside(self, point, frame_params):
        ret = True
        x, y, w, h = frame_params
        x1, y1 = point
        if x < x1 < x + w and y < y1 < y + h:
            ret = False
        return ret

    #   Update tracker and get speed for each car
    def update(self, objects_rect, gray_frame, frame_param):
        objects_bbs_ids = []
        speed = {}

        #   If we already have points to follow
        if self.vehicles.items():

            #   Calculate new position of points
            for _, car in self.vehicles.items():
                prepared_points = np.array([car.get_point()], dtype=np.float32)
                new_points2, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                            prepared_points, None, **self.lk_params)
                car.update_point(new_points2[0])

            #   Remove points outside of frame
            ids = []
            for _, car in self.vehicles.items():
                point = car.get_point()
                id = car.get_info()[4]
                if self.point_outside(point, frame_param):
                    ids.append(id)

            for id in ids:
                self.vehicles.pop(id, None)

            #   Get point speed
            for _, car in self.vehicles.items():
                id = car.get_info()[4]
                pt = car.get_point()
                speed[id] = self.speedEst.measure_speed2(id, pt)


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
                objects_bbs_ids.append(tmp_vehicle.get_info())
                speed[self.id_count] = 0
                self.id_count += 1

        #   Save frame for next step
        self.old_gray = gray_frame
        return objects_bbs_ids, speed
