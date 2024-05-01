import time
import math
from doodles import Circle, Color, Line, Group


def color_func(t):
    cycle = [Color.RED, Color.ORANGE, Color.GREEN, Color.BLUE]
    return cycle[int(t) % 4]


def size_func_factory(min_size, factor):
    def size_function(t):
        return math.sin(t) * factor + min_size

    return size_function


def create():
    g = Group().pos(400, 300)
    Circle(g).color(Color.BLACK).z(1).animate("radius", size_func_factory(260, 50))
    Circle(g).z(10).animate("color", color_func).animate(
        "radius", size_func_factory(250, 50)
    )
    Circle(g).radius(20).color(Color.BLACK).z(50)
    # Line(g).vec(
    #     lambda: time.time() % 60 / 60 * 360,
    #     200
    # ).z(100)

    l = Line(g).vec(0, 200).z(100).animate("degrees", lambda t: t % 60 / 60 * 360)
    # l.animate("color", color_func)
