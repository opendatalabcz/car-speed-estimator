import cv2
import numpy as np
from src import LPFinder as LPFinder
from src.speedMeasure import *
from src.vehicle import vehicle

class OpticalPointTracker:
    def __init__(self, gray, speed_measure):
        self.vehicles = {}
        self.id_count = 0
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.old_gray = gray
        self.speedEst = speed_measure

    #   Update tracker and get speed for each car
    def update(self, objects_rect, gray_frame, frame_param):
        objects_bbs_ids = []
        speed = {}

        #   If we already have points to follow
        if self.vehicles.items():

            #   Calculate new position of points
            for _, car in self.vehicles.items():
                prepared_points = car.get_prepared_points()
                new_points, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                            prepared_points, None, **self.lk_params)
                car.update_points(new_points)

            #   Remove vehicles outside of frame
            ids = []
            for _, car in self.vehicles.items():
                id = car.get_info()[4]
                if car.outside(frame_param):
                    ids.append(id)

            for id in ids:
                self.vehicles.pop(id, None)

            #   Get point speed
            for _, car in self.vehicles.items():
                id = car.get_info()[4]
                pt = car.get_points()
                speed[id] = self.speedEst.measure_speed(pt, id)


        #   Find match rectangles and points
        for rect in objects_rect:

            # Find out if that object was detected already
            same_object_detected = False
            if self.vehicles.items():
                for _, car in self.vehicles.items():
                    if car.check(rect):
                        car.update_rect(rect)
                        objects_bbs_ids.append(car.get_info())
                        car.nullify_counter()
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

        if self.vehicles.items():
            ids = []
            for _, car in self.vehicles.items():
                if car.counter() :
                    ids.append(car.get_info()[4])

            for id in ids:
                self.vehicles.pop(id, None)


        #   Save frame for next step
        self.old_gray = gray_frame
        return objects_bbs_ids, speed
