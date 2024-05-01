from doodles import Polygon, Color
import random


def new_point(t):
    return (random.random() * 100 - 50, random.random() * 100 - 50)


def create():
    for _ in range(5):
        p = Polygon().random(3)
        for pt in range(3):
            p.animate("point", new_point, to_modify=pt)
        p = Polygon().random(8)
        for pt in range(8):
            p.animate("point", new_point, to_modify=pt)
        p = Polygon().random(100)
        for pt in range(100):
            p.animate("point", new_point, to_modify=pt)
