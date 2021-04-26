import cv2
import numpy as np
from src.speedMeasure import *
from src.vehicle import vehicle
import csv

class OpticalPointTracker:
    def __init__(self, gray, frame_param, speed_measure):
        self.vehicles = {}
        self.vehicles_out = {}
        self.id_count = 0
        self.old_gray = gray
        self.speedEst = speed_measure
        self.frame_param = frame_param
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        #   Update tracker and get speed for each car
    def update(self, objects_rect, gray_frame):
        objects_bbs_ids = []
        speed = {}

        #   If we already have points to follow
        if self.vehicles.items():

            #   Calculate new position of points
            for _, car in self.vehicles.items():
                prepared_points = car.get_points()
                new_points, _, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, gray_frame,
                                                            prepared_points, None, **self.lk_params)
                car.update_points(new_points)

            #   Remove vehicles outside of frame
            ids = []
            for _, car in self.vehicles.items():
                id = car.get_info()[4]
                if car.outside(self.frame_param):
                    ids.append(id)

            for id in ids:
                self.vehicles_out[id] = self.vehicles[id].get_speed()
                self.vehicles.pop(id, None)

            #   Get point speed
            for _, car in self.vehicles.items():
                id = car.get_info()[4]
                pt = car.get_points()
                car.set_speed(self.speedEst.measure_speed(pt, id))
                speed[id] = car.get_speed()


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
                self.vehicles_out[id] = self.vehicles[id].get_speed()
                self.vehicles.pop(id, None)


        #   Save frame for next step
        self.old_gray = gray_frame
        return objects_bbs_ids, speed

    def create_csv(self):
        with open('Result.csv', 'w') as f:
            f.write("Id, Speed\n")
            for key in self.vehicles_out.keys():
                f.write("%s,%s\n" % (key, self.vehicles_out[key]))


class KcfTracker:
    def __init__(self, speed_measure):
        self.vehicles = {}
        self.vehicles_out = {}
        self.id_count = 0
        self.speedEst = speed_measure

    def update(self, objects_rect, frame):
        objects_bbs_ids = []
        speed = {}

        points = []

        if self.vehicles.items():
            print("-----------------")
            #   Update trackers
            for _, car in self.vehicles.items():
                car.update_rect2(frame)
                points.append(car.get_rectCenter())
                info = car.get_info2()
                print(info)
                if not info[0] == 0:
                    objects_bbs_ids.append(info)

        #   Find match rectangles and points
        for rect in objects_rect:
            x, y, w, h = rect
            # Find out if that object was detected already
            same_object_detected = False
            for point in points:
                if x < point[0] < x + w and y < point[1] < y + h:
                    same_object_detected = True
                    break

            # If new object is detected we assign the ID to that object
            if same_object_detected is False:
                tmp_vehicle = vehicle(rect, self.id_count)
                tmp_vehicle.create_tracker(frame)
                self.vehicles[self.id_count] = tmp_vehicle
                objects_bbs_ids.append(tmp_vehicle.get_info2())
                speed[self.id_count] = 0
                self.id_count += 1

        if self.vehicles.items():
            ids = []
            for _, car in self.vehicles.items():
                if car.counter() :
                    ids.append(car.get_info2()[4])

            for id in ids:
                self.vehicles_out[id] = self.vehicles[id].get_speed()
                self.vehicles.pop(id, None)


        #   Save frame for next step
        return objects_bbs_ids, speed

    def create_csv(self):
        with open('Result.csv', 'w') as f:
            f.write("Id, Speed\n")
            for key in self.vehicles_out.keys():
                f.write("%s,%s\n" % (key, self.vehicles_out[key]))