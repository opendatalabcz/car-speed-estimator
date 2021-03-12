from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class SpeedMeasure:

    def __init__(self, first_line, second_line, length):
        self.fps = 30
        self.list = {}
        self.length = length
        self.area = Polygon([first_line[0], first_line[1], second_line[1], second_line[0]])

    def in_area(self, point):
        p = Point(point[0], point[1])
        return self.area.contains(p)

    # mesure speed for each point
    def measure_speed(self, points):
        ret = {}
        for id, pt in points.items():

            # If point is not new
            if id in self.list:
                #   If points is inside of measuring area
                if self.in_area(pt):
                    self.list[id][0] = self.list[id][0] + 1
                    ret[id] = self.list[id][1]
                else:

                    #   If points just left measuring area
                    if self.list[id][0] != 0:
                        self.list[id][1] = int(self.length / (self.list[id][0] / self.fps) * 3.6)
                        self.list[id][0] = 0
                ret[id] = self.list[id][1]

            #   If its new add to list a return default number
            else:
                self.list[id] = [0, 0]
                ret[id] = 0

        return ret
