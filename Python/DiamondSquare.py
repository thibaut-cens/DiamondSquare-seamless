import random
from math import ceil, log2
from statistics import mean
import numpy


class DiamondSquare:

    @staticmethod
    def get_correct_size(size):
        max_size = max(size)
        effective_size = pow(2, ceil(log2(max_size - 1))) + 1
        return effective_size

    @staticmethod
    def middle_point(point_a, point_b):
        lw_x = min(point_a[0], point_b[0])
        up_x = max(point_a[0], point_b[0])
        lw_y = min(point_a[1], point_b[1])
        up_y = max(point_a[1], point_b[1])
        return [int(lw_x + (up_x - lw_x)/ 2), int(lw_y + (up_y - lw_y) / 2)]

    def clipPosition(self, pos):
        def circleValue(val, maxi):
            return maxi - val if val < 0 else val

        if pos[0] < 0:
            if self.seamless:
                pos[0] = circleValue(pos[0], self.DS_size)
            else:
                return None
        if pos[1] < 0:
            if self.seamless:
                pos[0] = circleValue(pos[0], self.DS_size)
            else:
                return None
        return pos

    def calculate_displace(self, points):
        neighbour_val = []
        for pos in points:
            neighbour_val.append(self.DS_array[int(pos[0]), int(pos[1])])
        average = mean(neighbour_val)
        displace = average + random.uniform(-0.5, 0.5)
        return displace

    def DiamondStep(self, point, size):
        neighbour = [[point[0] - size/2, point[1] - size/2],
                     [point[0] + size/2, point[1] - size/2],
                     [point[0] + size/2, point[1] + size/2],
                     [point[0] - size/2, point[1] + size/2]]
        neighbour = list(filter(None, [self.clipPosition(pos) for pos in neighbour]))
        self.DS_array[int(point[0]), int(point[1])] = self.calculate_displace(neighbour)

        next_steps = []
        if size > 1:
            for i in range(4):
                next_steps.append(self.middle_point(neighbour[i], neighbour[(i + 1) % len(neighbour)]))
        return next_steps

    def __init__(self, size, roughness, falloff, seamless=False, seed=None):
        self.size = [-1, -1]
        if not hasattr(size, '__iter__'):
            # it's not iterable, so it's probably an int
            self.size[0] = size
            self.size[1] = size
        else:
            self.size[0] = size[0]
            self.size[1] = size[1]

        self.roughness = roughness
        self.falloff = falloff
        self.seed = seed
        self.seamless = seamless

        if seed is not None:
            random.seed(seed)

        self.DS_size = self.get_correct_size(self.size)

        self.DS_array = numpy.zeros((self.DS_size, self.DS_size))
        self.DS_array *= -1.0

        self.DS_array[0, 0] = random.uniform(0, 1)
        self.DS_array[self.DS_size - 1, 0] = random.uniform(0, 1)
        self.DS_array[0, self.DS_size - 1] = random.uniform(0, 1)
        self.DS_array[self.DS_size - 1,
                      self.DS_size - 1] = random.uniform(0, 1)

        first = self.middle_point((0, 0), (self.DS_size - 1, self.DS_size - 1))
        current = [first]
        for i in range(ceil(log2(self.DS_size - 1))):
            nxt = []
            s = int((self.DS_size - 1) / 2 ** i)
            for c in current:
                nxt.append(self.DiamondStep(c, s))
            current = nxt
            nxt = []