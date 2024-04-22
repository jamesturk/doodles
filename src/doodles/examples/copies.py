from doodles import Group, Circle, Color

def original():
    g = Group()
    c = Circle(g).radius(80).color(Color.RED).pos(0, 0)
    for _ in range(15):
        c = c.copy().move(45, 45)
    return g

def create():
    r = original()
    r.copy().move(200, 0).color(Color.GREEN)
    r.copy().move(400, 0).color(Color.BLUE)
