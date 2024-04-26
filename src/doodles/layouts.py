"""
Experimental ideas for defining layouts.
"""

def make_grid(iterable, cols, rows, width, height, *, x_offset=0, y_offset=0):
    """
    This function attempts to create an evenly-spaced grid of drawables.

    The drawables are provided in an iterable, and when the iterable
    runs out of items the grid stops.

    A lot more behavior could be offered here, but this was
    done to validate the concept.

    By using an iterable here, it is possible to pass in lists that are
    too big or too small, and the grid will still work.
    (Leaving empty slots empty, or not drawing extras depending on the
    relationship of the grid size to the iterable.)

    Another neat trick is using an infinite generator (as done in examples/grid)
    since only as many doodles as needed to fill the grid will be gathered.
    """
    try:
        for c in range(cols):
            for r in range(rows):
                doodle = next(iterable)
                doodle.pos(width * c + x_offset, height * r + y_offset)
    except StopIteration:
        pass
