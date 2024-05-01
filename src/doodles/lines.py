"""
Class to draw lines.

This is the most well-documented version of a concrete doodle,
the easiest to learn from.
"""
import math
import random
from typing import Self
from .doodles import Doodle
from .world import world


class Line(Doodle):
    # Adds one attribute to Doodle: the distance/offset vector
    # from the position.  Together these form the end points of the
    # line.
    _offset_vec: tuple[float, float]

    def __init__(self, parent=None):
        """
        We keep the same interface as Doodle, to follow the Liskov substitution
        principle.

        We could add more *optional* arguments, but no more required ones
        than the parent class.
        """
        super().__init__(parent)
        # a line is stored as a position (on the parent class)
        # and an offset vector
        self._offset_vec = (10, 0)

    def __repr__(self):
        return f"Line(pos={self.world_vec}, end={self.end_vec}, {self._color})"

    def draw(self):
        """
        Implementation of the abstract draw function for the line.

        This class passes the responsibility of actually drawing to
        the world.draw_engine, which is designed to be configurable.

        An earlier version had Pygame drawing code in here, but that
        violated the Single Responsibility Principle.

        Instead, as a pass-through, the actual drawing logic is not coupled
        to the mathematical representation of a line.
        """
        world.draw_engine.line_draw(self)

    ## Setters / Modifiers / Getters ##############

    def to(self, x: float, y: float) -> Self:
        """
        A setter for the line's offset vector.

        Example usage:

        Line().pos(10, 10).to(50, 50)

        Makes a line from (10, 10) to (50, 50).
        """
        self._offset_vec = (x, y)
        return self

    def vec(self, degrees: float, magnitude: float):
        """
        Alternate setter, to create offset vector from angle & length.

        This is similar to the constructor/alternate constructor concept
        where there's a base constructor that sets the propertries
        directly (`to`), but there is also an alternate option
        that handles commonly used case.
        """
        return self.to(
            magnitude * math.cos(math.radians(degrees)),
            magnitude * math.sin(math.radians(degrees)),
        )

    def degrees(self, degrees: float):
        """
        Alternate setter, like calling vec(new_degrees, old_magnitude).
        """
        magnitude = math.sqrt(self._offset_vec[0] ** 2 + self._offset_vec[1] ** 2)
        return self.to(
            magnitude * math.cos(math.radians(degrees)),
            magnitude * math.sin(math.radians(degrees)),
        )

    def random(self) -> Self:
        """
        Overrides the parent's random, since a random line
        also needs to have a offset vector.

        This is an example of the **Open/Closed Principle**.
        We aren't modifying the parent classes' random function
        since doing so would be fragile and break if the
        parent class added more options.

        Instead we just call it, and extend it with additional
        randomization.
        """
        super().random()
        magnitude = random.random() * 100
        degrees = random.random() * 360
        return self.vec(degrees, magnitude)

    @property
    def end_vec(self):
        """
        Line goes from world_x, world_y to this position which
        results from adding (world_x, world_y) + (offset_x, offset_y).
        """
        return (
            self.world_x + self._offset_vec[0],
            self.world_y + self._offset_vec[1],
        )
