import numpy as np
import cv2
import ellipse
import math

class CharacterLocation:
    
    def __init__(self, points):
        self.points = points
        mean = self.points.mean(axis=0)
        self.center = [int(round(p)) for p in mean]

    @property
    def extremes(self):
        min_x, max_x, min_y, max_y = None, None, None, None
        for x, y in self.points:
            min_x = min(x, min_x) if min_x else x
            max_x = max(x, max_x) if max_x else x
            min_y = min(y, min_y) if min_y else y
            max_y = max(y, max_y) if max_y else y
        return min_x, max_x, min_y, max_y        

def is_likely_duplicate(l1: CharacterLocation, l2: CharacterLocation):
    return point_distance(l1.center, l2.center) < 30

def point_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    asquared = (x2 - x1) ** 2
    bsquared = (y2 - y1) ** 2
    return math.sqrt(asquared + bsquared)

def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    rise = y1 - y2
    run = x1 - x2
    return rise / run

def merge_locations(locations):
    merged = []
    foo = 8 #todo: think of a real name, idiot
    for loc in locations:
        print(cv2.isContourConvex(loc.points))
        front_slope = slope(loc.points[foo - 1], loc.points[0]) #y
        front_slope_inverse = 1 / front_slope #x
        line = []
        startx, starty = loc.points[0]
        for i in range(1, 21):
            incx, incy = i * front_slope_inverse, i * front_slope
            line.append((startx - incx, starty - incy))
        loc.points = np.concatenate((np.array(line).astype(int), loc.points))
        end_slope = slope(loc.points[0], loc.points[foo - 1])
        merged.append(loc)
    return merged