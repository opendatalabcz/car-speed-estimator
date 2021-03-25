from src.LPFinder import *
import numpy as np

class vehicle:

    def __init__(self, rect, id):
        self.rect = rect
        x, y, w, h = rect
        self.area = w * h
        self.point = []
        self.points = []
        self.id = id
        self.out = 0

    def create_points(self, frame):
        x, y, w, h = self.rect
        object_img = frame[y:y + h, x:x + w]
        self.point = []
#           LPFinder
        px, py = FindLP(object_img)
        self.point = [x + px, y + py]
        self.points.append([x + px, y + py])
#          Central point
        self.points.append([x + (w//2), y + (h//2)])
#          Biggest area
#          Licence plate
#          Upper part
        self.points.append([x + (w//2), y + (h//4)])

    def check(self, rect):
        ret = False
        check = 0;
        x, y, w, h = rect

        for pt in self.points:
            if x < pt[0] < x + w and y < pt[1] < y + h :
                check += 1

        if check > 1:
            ret = True
        return ret

    def get_points(self):
        return self.points

    def update_points(self, points):
        self.points = points
        self.point = points[0]

    def get_info(self):
        x, y, w, h = self.rect
        return [x, y, self.point[0], self.point[1], self.id]

    def update_rect(self, rect):
        self.rect = rect

    def get_prepared_points(self):
        prepared_points = np.array(self.points, dtype=np.float32)
        return prepared_points

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

    def counter(self):
        ret = False
        self.out += 1
        if (self.out > 30):
            ret = True
        return ret

    def nullify_counter(self):
        self.out = 0
