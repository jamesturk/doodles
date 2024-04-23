from doodles import Group, Circle, Color

def tri():
    g = Group()
    Circle(g).radius(50).color(Color.RED).pos(0, 0).alpha(128)
    Circle(g).radius(50).color(Color.GREEN).pos(-25, 35).alpha(128)
    Circle(g).radius(50).color(Color.BLUE).pos(25, 35).alpha(128)
    return g

def create():
    r = tri().move(200, 200)
