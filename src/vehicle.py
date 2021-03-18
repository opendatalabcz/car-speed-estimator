from src.LPFinder import *

class vehicle:

    def __init__(self, rect, id):
        self.rect = rect
        x, y, w, h = rect
        self.area = w * h
        self.point = []
        self.id = id

    def create_points(self, frame):
        x, y, w, h = self.rect
        object_img = frame[y:y + h, x:x + w]
        self.point = []
#          Central point
        px, py = FindLP(object_img)
        self.point = [x + px, y + py]

#          Biggest area
#          Licence plate
#          Upper part

    def check(self, rect):
        ret = False
        check = 0;
        x, y, w, h = rect

        for pt in self.points:
            if x < pt[0] < x + w and y < pt[1] < y + h:
                check += 1

        if check > 1:
            ret = True
        return ret

    def get_point(self):
        return self.point

    def update_point(self, points):
        self.point = points

    def get_info(self):
        x, y, w, h = self.rect
        return [x, y, self.point[0], self.point[1], self.id]

    def update_rect(self, rect):
        self.rect = rect