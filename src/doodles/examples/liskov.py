"""
Demo of the interchangable nature of these classes.
"""
from doodles import Polygon, Line, Rectangle, Circle
import random
import math

types = [Polygon, Line, Rectangle, Circle]


def rainbow(t) -> tuple[int, int, int]:
    """cycles through colors based on time"""
    t = t % 1.0

    r = int(255 * (1 + math.sin(2 * math.pi * (t + 0.0 / 3))) / 2)
    g = int(255 * (1 + math.sin(2 * math.pi * (t + 1.0 / 3))) / 2)
    b = int(255 * (1 + math.sin(2 * math.pi * (t + 2.0 / 3))) / 2)

    return (r, g, b)


def create():
    for _ in range(100):
        DoodleType = random.choice(types)
        d = DoodleType()
        # we do not need to know what DoodleType is, these methods all work
        d.random().animate("color", rainbow)
