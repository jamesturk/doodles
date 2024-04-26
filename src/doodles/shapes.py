"""
Adds more drawables, like `lines`.  For the most part
these classes only differ from `Line` in implementation.

The interface & decisions are the same but specific
to `Circle` and `Rectangle`.
"""
import random
from .doodles import Doodle
from .world import world


class Circle(Doodle):
    def __init__(self, parent=None):
        super().__init__(parent)
        # circle is a position & radius
        self._radius = 0

    def __repr__(self):
        return f"Circle(pos={self.world_vec}, radius={self._radius}, {self._color}, parent={self._parent}))"

    def draw(self):
        # TODO: do we need to override draw? can we move this to Doodle.draw
        world.draw_engine.circle_draw(self)

    def radius(self, r: float) -> "Doodle":
        """
        A setter for the circle's radius.
        """
        self._radius = r
        return self

    @property
    def radius_val(self) -> float:
        return self._radius

    def grow(self, by: float):
        """
        Modify radius by an amount. (Negative to shrink.)
        """
        return self.radius(self._radius + by)

    def random(self) -> "Doodle":
        super().random()
        # constrain to 10-100
        return self.radius(random.random() * 90 + 10)


class Rectangle(Doodle):
    def __init__(self, parent=None):
        """
        For compatibility with circle, the rectangle is centered at pos
        and expands out width/2, height/2 in each cardinal direction.
        """
        super().__init__(parent)
        self._width = 100
        self._height = 100

    def __repr__(self):
        return f"Rect(pos={self.world_vec}, width={self._width}, height={self._height}, parent={self._parent})"

    def draw(self):
        world.draw_engine.rect_draw(self)

    def width(self, w: float) -> "Doodle":
        """
        Set new width.
        """
        self._width = w
        return self

    def height(self, h: float) -> "Doodle":
        """
        Set new height.
        """
        self._height = h
        return self

    def grow(self, dw: float, dh: float):
        return self.width(self._w + dw).height(self._h + dh)

    def random(self, upper=100) -> "Doodle":
        super().random()
        # constrain to 10-100
        return self.width(random.random() * upper + 10).height(
            random.random() * upper + 10
        )
