from abc import ABC, abstractmethod
import sys
import copy
import random
import math
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 600


class Doodle(ABC):
    def __init__(self):
        self._pos_vec = (0, 0)
        self._color = BLACK

    @abstractmethod
    def draw(self, screen) -> None:
        pass

    def copy(self):
        return copy.copy(self)

    def color(self, r, g, b):
        self._color = (r, g, b)
        return self

    def pos(self, x, y):
        self._pos_vec = (x, y)
        return self

    def move(self, dx, dy):
        return self.pos(self.x + dx, self.y + dy)

    def random(self):
        x = random.random() * WIDTH
        y = random.random() * HEIGHT
        r = random.random() * 255
        g = random.random() * 255
        b = random.random() * 255
        return self.pos(x, y).color(r, g, b)

    @property
    def pos_vec(self):
        return self._pos_vec

    @property
    def x(self):
        return self._pos_vec[0]

    @property
    def y(self):
        return self._pos_vec[1]


class Line(Doodle):
    def __init__(self):
        super().__init__()
        self._offset_vec = (10, 0)

    def __repr__(self):
        return f"Line(pos={self.pos_vec}, end={self.end_vec}, {self._color})"

    def draw(self, screen):
        pygame.draw.line(screen, self._color, self.pos_vec, self.end_vec)

    def to(self, x, y):
        self._offset_vec = (x, y)
        return self

    def random(self):
        super().random()
        magnitude = random.random() * 100
        degrees = random.random() * 360
        return self.vec(degrees, magnitude)

    def vec(self, degrees, magnitude):
        return self.to(magnitude * math.cos(math.radians(degrees)),
                        magnitude * math.sin(math.radians(degrees)))

    @property
    def end_vec(self):
        return (self.pos_vec[0] + self._offset_vec[0],
                self.pos_vec[1] + self._offset_vec[1],
                )

class Group(Doodle):
    def __init__(self):
        super().__init__()
        self._doodles = []

    def draw(self, screen):
        for d in self._doodles:
            d.draw(screen)

    def color(self, r, g, b):
        for d in self._doodles:
            d.color(r, g, b)

    def copy(self):
        return copy.deepcopy(self)

    def add(self, doodle):
        self._doodles.append(doodle)
        return self

    def move(self, dx, dy):
        for d in self._doodles:
            d.move(dx, dy)
        return self

def render_scene(screen, background, *drawables):
    screen.fill(background)
    for d in drawables:
        d.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Doodles")

    g = Group()
    for d in range(100, 200, 10):
        g.add(
            Line().pos(300, 300).vec(d, 100)
        )

    g2 = g.copy()
    g2.move(20, 20)
    g3 = g.copy()
    g3.move(100, 100).color(0, 100, 100)
    g3.add(Line().random().pos(g3.x, g3.y))
    g3.add(Line().random().pos(g3.x, g3.y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        render_scene(screen, WHITE, g, g2, g3)

        pygame.display.flip()

if __name__ == "__main__":
    main()
