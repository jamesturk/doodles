from .color import Color
import pygame

class World:
    """
    This class is a singleton, only one instance should ever exist.

    A common reason for this is a class that manages a resource of some kind,
    in this case, our screen.
    This class needs to track where entities are in relation to the screen,
    and will hold a reference to a pygame variable that lets it draw to the screen.

    Multiple instances of this class would

    There are two schools of thought about this pattern:

    You can use this pattern as we do here, with no extra code.
    We instead define an instance variable "world" below, and
    documentation would show users to use that global variable.
    It would technically be possible for someone to instantiate
    a "world2 = World()" instance, but doing so would be admonished
    in documentation and not supported.

    You could optionally denote this by naming the class _World.

    Others prefer to have code-level enforcement of this policy.
    There's a nearly infinite number of ways to do this, including
    simply keeping a global "_instance_created" variable that gets
    set to a non-None value after first creation, and then
    raises an exception on invalid use, or with a bit of cleverness
    returns the single-instance no matter how hard the user
    tries to create a new one.
    """

    WIDTH = 800
    HEIGHT = 600
    _instance = None

    def __init__(self):
        # This logic forms the basis of a check for prior instances.
        # Code could be added here to explicitly disallow them.
        if self._instance is None:
            self._instance = self
        self._drawables = []
        self.background_color = Color.WHITE
        self.screen = None

    def init(self):
        """
        Delayed initialization, can't be run at start
        but must be run once.
        """
        if self.screen:
            raise ValueError("Can't initialize world twice!")
        self.screen = pygame.display.set_mode((world.WIDTH, world.HEIGHT))

    def add(self, drawable):
        self._drawables.append(drawable)

    def tick(self):
        for d in self._drawables:
            d.update()

    def render(self):
        """
        Draw world to screen
        """
        self.screen.fill(self.background_color)
        for d in sorted(self._drawables, key=lambda d: d._z_index):
            d.draw(self.screen)


# our singleton instance
world = World()

