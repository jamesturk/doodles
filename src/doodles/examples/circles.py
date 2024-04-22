from doodles.doodles import Group, Circle, Color
from doodles.world import world

def create():
    g = Group().pos(400, 300)
    for r in range(20, 50, 5):
        Circle(g).radius(r).color(Color.random()).z_index(-r)
    for r in range(60, 150, 10):
        Circle(g).radius(r).color(Color.random()).z_index(-r)
