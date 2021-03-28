from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

#   Class for measuring speed of vehicles
class SpeedMeasure:

    #   Constructor
    def __init__(self, first_line, second_line, length, fps):
        self.fps = fps
        self.list = {}
        self.length = length
        self.area = Polygon([first_line[0], first_line[1], second_line[1], second_line[0]])

    #   Function for checking if point is in measured area
    def in_area(self, point):
        p = Point(point[0], point[1])
        return self.area.contains(p)

    #   Function for measuring speed of vehicle
    def measure_speed(self, points, id):
        cnt = 0
        out = 0

        #   If vehicle is new than create new item in list and return speed 0
        if not id in self.list:
            self.list[id] = [0, 0, 0, 0]
            return 0

        #   Check for each point if they are in measured area or not
        for pt in points:
            cnt += 1

            #   If points is inside of measuring area than increase timer
            if self.in_area(pt):
                self.list[id][cnt] = self.list[id][cnt] + 1
            else:

            #   If point is outside of measuring area
                out += 1

        #   If all points are outside of measuring area
        if out == 3:

            #   If vehicle doesnt have its speed calculated and each point was measured.
            if self.list[id][0] == 0 and self.list[id][1] != 0 and self.list[id][2] != 0 and self.list[id][3] != 0:
                tmp = 0

                #   Caculate speed for each point and then make avarege
                for i in range (1, 4):
                    tmp += int(self.length / (self.list[id][i] / self.fps) * 3.6)
                    self.list[id][i] = 0
                self.list[id][0] = int(tmp/3)

        return self.list[id][0]