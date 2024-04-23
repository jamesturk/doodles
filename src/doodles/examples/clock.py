import time
from doodles import Circle, Color, Line, Group

def create():
    g = Group().pos(400, 300)
    Circle(g).radius(300).color(Color.BLACK).z(1)
    Circle(g).radius(290).color(Color.BROWN).z(10)
    Circle(g).radius(20).color(Color.BLACK).z(50)
    Line(g).vec(lambda: time.time() % 60 / 60 * 360, 200).z(100)
