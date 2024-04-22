from doodles import Group, Circle, Color

def color_cycle():
    while True:
        yield Color.RED
        yield Color.ORANGE
        yield Color.YELLOW

def create():
    color = color_cycle()
    g = Group().pos(400, 300)
    for r in range(20, 100, 12):
        Circle(g).radius(r).color(next(color)).z_index(-r)
    for r in range(100, 250, 12):
        Circle(g).radius(r).color(next(color)).z_index(-r)
