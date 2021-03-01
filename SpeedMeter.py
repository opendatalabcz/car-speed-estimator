import math

class SpeedEstimator:

    def __init__(self, y_first_line, y_second_line):
        if y_first_line < y_second_line:
            self.line1 = y_first_line
            self.line2 = y_second_line
        else:
            self.line1 = y_second_line
            self.line2 = y_first_line
        self.meter_per_pixel = (self.line2 - self.line1)/5
        self.fps = 30
        self.list = {}

    def estimate_speed(self, points):
        ret = {}

        for id, pt in points.items():
            if id in self.list:
                if self.line1 < pt[1] < self.line2:
                    self.list[id][0] = self.list[id][0] + 1
                    ret[id] = self.list[id][1]
                else:
                    if self.list[id][0] != 0:
                        self.list[id][1] = int(10/(self.list[id][0]/self.fps) * 3.6)
                        self.list[id][0] = 0
                ret[id] = self.list[id][1]
            else:
                self.list[id] = [0, 0]
                ret[id] = 0

        return ret