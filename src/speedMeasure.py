from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class SpeedMeasure:

    def __init__(self, first_line, second_line, length, fps):
        self.fps = fps
        self.list = {}
        self.length = length
        self.area = Polygon([first_line[0], first_line[1], second_line[1], second_line[0]])

    def in_area(self, point):
        p = Point(point[0], point[1])
        return self.area.contains(p)

    def measure_speed(self, points, id):
        cnt = 0
        out = 0
        if not id in self.list:
            self.list[id] = [0, 0, 0, 0]
            return 0
        print(self.list[id])
        for pt in points:
            cnt += 1
            #   If points is inside of measuring area
            if self.in_area(pt):
                self.list[id][cnt] = self.list[id][cnt] + 1
            else:
            #   If point is outside of measuring area
                out += 1

        #   If all points are outside of measuring area
        if out == 3:
            if self.list[id][0] == 0 and self.list[id][1] != 0 and self.list[id][2] != 0 and self.list[id][3] != 0:
                tmp = 0
                for i in range (1, 4):
                    tmp += int(self.length / (self.list[id][i] / self.fps) * 3.6)
                    self.list[id][i] = 0
                self.list[id][0] = int(tmp/3)

        return self.list[id][0]