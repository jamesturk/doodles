

def make_grid(iterable, cols, rows, width, height, *, x_offset=0, y_offset=0):
    """
    Arranges the objects in iterable in a grid with the given parameters.
    """
    try:
        for c in range(cols):
            for r in range(rows):
                doodle = next(iterable)
                doodle.pos(width * c + x_offset, height * r + y_offset)
    except StopIteration:
        pass
