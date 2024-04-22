from doodles.doodles import Group, Line
from doodles.layouts import make_grid

def same_spiral():
    while True:
        # Create a group of lines all with same origin, different angles.
        g = Group()
        for d in range(0, 180, 10):
            Line(g).vec(d, 200 - d)
        yield g

def create():
    # Make copies, moving each one and modifying the color
    make_grid(same_spiral(), 3, 4, 250, 140, x_offset=70, y_offset=20)
