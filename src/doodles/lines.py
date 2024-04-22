import math
import random
import pygame
from typing import Callable
from .doodles import Doodle


class Line(Doodle):
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
        return f"Line(pos={self.pos_vec}, end={self.end_vec}, {self._color})"

    def draw(self, screen):
        """
        Implementation of the abstract draw function for the line.

        Note: This is a classic violation of single responsibility.

        Instead, you could imagine a class like:

        class DrawingBackend:
            def draw_doodle(doodle_type, doodle): ...

        class PygameBackend(DrawingBackend):
            def draw_line(...): ...

        This would make it possible to attach different
        drawing backends, restoring single-responsibility
        to the class and gaining flexibility from separating
        presentation logic from data manipulation.
        """
        pygame.draw.aaline(screen, self._color, self.pos_vec, self.end_vec)

    def to(self, x: float, y: float) -> "Doodle":
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
        Alternate constructor, to create offset vector from angle & length.
        """
        if isinstance(degrees, Callable):
            self.register_update(
                self.to,
                lambda: magnitude * math.cos(math.radians(degrees())),
                lambda: magnitude * math.sin(math.radians(degrees())),
            )
            return self

        return self.to(
            magnitude * math.cos(math.radians(degrees)),
            magnitude * math.sin(math.radians(degrees)),
        )

    def random(self) -> "Doodle":
        """
        Overrides the parent's random, by extending the behavior.

        This is an example of the open/closed principle.
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
        Parallel to pos_vec for end of line.
        """
        return (
            self.x + self._offset_vec[0],
            self.y + self._offset_vec[1],
        )
