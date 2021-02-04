import numpy as np

class manager:
    def __init__(self, shape):
        self.points = []
        self.shape = shape

    def add_point(self, x, y):
        if self.check(x, y):
            self.points.append([x, y])

    def print(self):
        print(self.points)

    def rewrite(self, new_points):
        position = 0
        for point in new_points:
            x, y = point.ravel()
            if (abs(self.points[position][0] - x) + abs(self.points[position][1] - y)) > 0.1:
                self.points[position] = [x, y]
                position = position + 1
            else:
                self.points.pop(position)
#        self.print()
        self.erase_control()

    def check(self, x, y):
        for point in self.points:
            if abs(point[0] - x) < 20 or abs(point[1] - y) < 20:
                return False
        return True

    def get(self, position):
        if len(self.points) <= position:
            return []
        else:
            return self.points[position]

    def getAll(self):
        return np.array(self.points, dtype=np.float32)

    def point_selected(self):
        if len(self.points) > 0:
            return True
        else:
            return False

    def erase_control(self):
        position = 0
        for point in self.points:
            if (point[0] < 0) or (point[1] < 0) or (point[0] > self.shape[0]) or (point[1] > self.shape[1]):
                self.points.pop(position)
                position = position - 1
            position = position + 1