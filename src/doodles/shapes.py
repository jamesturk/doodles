"""
Adds more drawables, like `lines`.  For the most part
these classes only differ from `Line` in implementation.

The interface & decisions are the same but specific
to `Circle` and `Rectangle`.
"""
from typing import Self, Optional
import random
from .doodles import Doodle
from .world import world


class Circle(Doodle):
    def __init__(self, parent=None):
        super().__init__(parent)
        # circle is a position & radius
        self._radius = 0

    def __repr__(self):
        return f"Circle(pos={self.world_vec}, radius={self._radius}, {self._color})"

    def draw(self):
        # TODO: do we need to override draw? can we move this to Doodle.draw
        world.draw_engine.circle_draw(self)

    def radius(self, r: float) -> Self:
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

    def random(self) -> Self:
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
        return f"Rect(pos={self.world_vec}, width={self._width}, height={self._height})"

    def draw(self):
        world.draw_engine.rect_draw(self)

    def width(self, w: float) -> Self:
        """
        Set new width.
        """
        self._width = w
        return self

    def height(self, h: float) -> Self:
        """
        Set new height.
        """
        self._height = h
        return self

    def grow(self, dw: float, dh: float) -> Self:
        return self.width(self._width + dw).height(self._height + dh)

    def random(self, size: float = 100) -> Self:
        super().random()
        # constrain to 10-100
        return self.width(random.random() * size + 10).height(
            random.random() * size + 10
        )


class Polygon(Doodle):
    """
    All points are *relative* to the center point.
    That is to say, if you had a triangle with coordinates:

        (100, 100)
        (0, 100)
        (-100, 0)

    And the object was moved to (50, 50), the actual triangle drawn
    on screen would be:

        (150, 150)
        (50, 150)
        (50, 50)
    """

    _points: list[tuple[float, float]]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._points = []

    def __repr__(self):
        return f"Polygon(pos={self.world_vec}, points={self._points})"

    def draw(self):
        world.draw_engine.polygon_draw(self)

    def point(
        self, point: tuple[float, float], to_modify: Optional[int] = None
    ) -> Self:
        if to_modify is not None:
            self._points[to_modify] = point
        else:
            self._points.append(point)
        return self

    def random(self, n_points: int) -> Self:
        super().random()
        for _ in range(n_points):
            self.point((random.random() * 100 - 50, random.random() * 100 - 50))
        return self
