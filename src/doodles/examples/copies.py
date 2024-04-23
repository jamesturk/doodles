from doodles import Group, Circle, Color

def create():
    g = Group()
    c = Circle(g).radius(80).color(Color.RED).pos(0, 0)
    for _ in range(15):
        c = c.copy().move(45, 45)
    g.copy().move(200, 0).color(Color.GREEN)
    g.copy().move(400, 0).color(Color.BLUE)
