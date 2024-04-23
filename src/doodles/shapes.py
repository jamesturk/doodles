import random
import pygame
from .doodles import Doodle


class Circle(Doodle):
    def __init__(self, parent=None):
        """
        This is a less interesting class than Line, but very similar.
        """
        super().__init__(parent)
        # circle is a position & radius
        self._radius = 0

    def __repr__(self):
        return f"Circle(pos={self.world_vec}, radius={self._radius}, {self._color}, parent={self._parent}))"

    def draw(self, screen):
        pygame.draw.circle(screen, self.rgba, self.world_vec, self._radius)

    def radius(self, r: float) -> "Doodle":
        """
        A setter for the circle's radius.
        """
        self._radius = r
        return self

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

    def draw(self, screen):
        rect = pygame.Rect(
            self.world_x - self._width / 2,
            self.world_y - self._height / 2,
            self._width,
            self._height,
        )
        pygame.draw.rect(screen, self._color, rect)

    def width(self, w: float) -> "Doodle":
        """
        A setter for the width
        """
        self._width = w
        return self

    def height(self, h: float) -> "Doodle":
        """
        A setter for the height
        """
        self._height = h
        return self

    def grow(self, dw: float, dh: float):
        """
        Modify radius by an amount. (Negative to shrink.)
        """
        return self.width(self._w + dw).height(self._h + dh)

    def random(self, upper=100) -> "Doodle":
        super().random()
        # constrain to 10-100
        return self.width(random.random() * upper + 10).height(
            random.random() * upper + 10
        )
