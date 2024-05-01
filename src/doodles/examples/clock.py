import time
from doodles import Circle, Color, Line, Group


def color_func(t):
    print("updating color")
    cycle = [Color.RED, Color.ORANGE, Color.GREEN, Color.BLUE]
    return cycle[int(t) % 4]


def create():
    g = Group().pos(400, 300)
    Circle(g).radius(300).color(Color.BLACK).z(1)
    Circle(g).radius(290).color(Color.BROWN).z(10)
    Circle(g).radius(20).color(Color.BLACK).z(50)
    # Line(g).vec(
    #     lambda: time.time() % 60 / 60 * 360,
    #     200
    # ).z(100)

    l = Line(g).vec(0, 200).z(100).animate("degrees", lambda t: t % 60 / 60 * 360)
    l.animate("color", color_func)
