"""
Demo of the interchangable nature of these classes.
"""
from doodles import Polygon, Line, Rectangle, Circle, Color
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
        doodle = DoodleType().random().animate("color", rainbow)
