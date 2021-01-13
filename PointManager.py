import numpy as np

class manager:
    def __init__(self):
        self.points = []

    def add_point(self, x, y):
        if self.check(x, y):
            self.points.append([x, y])

    def print(self):
        print(self.points)

    def rewrite(self, position, x, y):
        self.points[position] = [x, y]

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
