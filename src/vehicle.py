from src.LPFinder import *
import numpy as np

#   Class for vehicles founded in video file
class vehicle:

    #   Constructor
    def __init__(self, rect, id):
        self.rect = rect
        self.points = []
        self.id = id
        self.out = 0

    #   Create points of interest on vehicle
    def create_points(self, frame):
        x, y, w, h = self.rect
        object_img = frame[y:y + h, x:x + w]
#           LPFinder
        px, py = FindLP(object_img)
        self.points.append([x + px, y + py])
#          Central point
        self.points.append([x + (w//2), y + (h//2)])
#          Upper part
        self.points.append([x + (w//2), y + (h//4)])
        self.points = np.array(self.points, dtype=np.float32)

    #   Return if rectangle can be from this vehicle
    def check(self, rect):
        ret = False
        check = 0;
        x, y, w, h = rect

        #   Check if points are inside rectangle
        for pt in self.points:
            if x < pt[0] < x + w and y < pt[1] < y + h :
                check += 1

        #   If at least 2 points are inside then return true
        if check > 1:
            ret = True
        return ret

    #   Getter for vehicle points of interest
    def get_points(self):
        return self.points

    #   Update vehicle points of interests
    def update_points(self, points):
        self.points = points

    #   Return information about vehicle
    def get_info(self):
        x, y, _, _ = self.rect
        return [x, y, self.points[0][0], self.points[0][1], self.id]

    #   Update vehicle rectangle
    def update_rect(self, rect):
        self.rect = rect

    #   Return if vehicle is outside of frame
    def outside(self, frame_param):
        _, _, w, h = frame_param
        cnt = 0
        ret = True
        for pt in self.points:
            if 0 < pt[0] < w and 0 < pt[1] < h :
                cnt += 1
        if cnt == 3:
            ret = False
        return ret

    #   Increment counter for missing vehicle and return value if vehicle is missing too long
    def counter(self):
        ret = False
        self.out += 1
        if (self.out > 30):
            ret = True
        return ret

    #   Nullify counter for missing vehicle
    def nullify_counter(self):
        self.out = 0
