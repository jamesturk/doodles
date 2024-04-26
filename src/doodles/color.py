import random


class Color:
    """
    This class is being used as a namespace, similar to an `enum.Enum` class.

    This is done to group many global variables into a namespace for clarity.

    There is no reason for anyone to ever declare an instance of this class.
    Instead it will be used like Color.BLACK.

    Another option would be to just have these be bare methods
    at the `color` module and encourage use like color.random()

    The two are equivalent, but this way was chosen as a demonstration
    and to make `from colors import random` impossible, since that would
    be confusing downstream.

    Palette Source: https://pico-8.fandom.com/wiki/Palette
    """

    BLACK = (0, 0, 0)
    DARK_BLUE = (29, 43, 83)
    PURPLE = (126, 37, 83)
    DARK_GREEN = (0, 135, 81)
    BROWN = (171, 82, 54)
    DARK_GREY = (95, 87, 79)
    LIGHT_GREY = (194, 195, 199)
    WHITE = (255, 241, 232)
    RED = (255, 0, 77)
    ORANGE = (255, 163, 0)
    YELLOW = (255, 236, 39)
    GREEN = (0, 228, 54)
    BLUE = (41, 173, 255)
    LAVENDER = (131, 118, 156)
    PINK = (255, 119, 168)
    LIGHT_PEACH = (255, 204, 170)

    def __init__(self):
        raise NotImplementedError("Color is not meant to be invoked directly")

    @staticmethod
    def all():
        colors = list(Color.__dict__.values())
        return [color for color in colors if isinstance(color, tuple)]

    @staticmethod
    def random():
        return random.choice(Color.all())
