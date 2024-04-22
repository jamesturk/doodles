from .world import world


def make_grid(iterable, cols, rows, width, height, *, x_offset=0, y_offset=0):
    """
    Arranges the objects in iterable in a grid with the given parameters.
    """
    try:
        doodle = next(iterable)
        for c in range(cols):
            for r in range(rows):
                doodle.pos(width * c + x_offset, height * r + y_offset)
                world.add(doodle)
                doodle = next(iterable)
    except StopIteration:
        pass


def copies(doodle):
    """
    Lazily makes an infinite number of copies of a given doodle.

    Can be combined with things like `make_grid` that require
    an iterable of doodles to repeat.
    """
    while True:
        yield doodle.copy()
