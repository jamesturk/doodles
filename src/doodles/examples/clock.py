import time
from doodles import Circle, Color, Line, Group

def create():
    g = Group().pos(400, 300)
    Circle(g).radius(300).color(Color.BLACK).z_index(1)
    Circle(g).radius(290).color(Color.BROWN).z_index(10)
    Circle(g).radius(20).color(Color.BLACK).z_index(50)
    Line(g).vec(lambda: time.time() % 60 / 60 * 360, 200).z_index(100)
