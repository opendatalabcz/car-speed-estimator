import math

class SpeedMeasure:

    def __init__(self, y_first_line, y_second_line):
        if y_first_line < y_second_line:
            self.line1 = y_first_line
            self.line2 = y_second_line
        else:
            self.line1 = y_second_line
            self.line2 = y_first_line
        self.fps = 30
        self.list = {}

    # mesure speed for each point
    def measure_speed(self, points):
        ret = {}
        for id, pt in points.items():

            # If point is not new
            if id in self.list:

                #   If points is inside or measuring area
                if self.line1 < pt[1] < self.line2:
                    self.list[id][0] = self.list[id][0] + 1
                    ret[id] = self.list[id][1]
                else:

                    #   If points just left measuring area
                    if self.list[id][0] != 0:
                        self.list[id][1] = int(10/(self.list[id][0]/self.fps) * 3.6)
                        self.list[id][0] = 0
                ret[id] = self.list[id][1]

            #   If its new add to list a return default number
            else:
                self.list[id] = [0, 0]
                ret[id] = 0

        return ret