"""
This is the most complex/implementation specific module.

TODO: this should be split into two modules once there
      is a non-Pygame implementation.
"""
from .color import Color
import pygame
from .draw_engine import DrawEngine


class PygameDrawEngine(DrawEngine):
    # Having each bit of text on the screen load a separate copy
    # of its font would be wasteful, since the most common case would
    # be for most text to use the same font.
    #
    # The solution here is to use a class attribute, shared by *all* instances
    # of the class.
    #
    # This is an implementation of the Flyweight design pattern, which
    # allows multiple objects to share some state.
    #
    # This can quickly become a mess if the shared state is mutable,
    # note that here, once a font is loaded it does not change.
    # This avoids nearly all pitfalls associated with this approach.
    _fonts: dict[str, pygame.font.Font] = {}
    DEFAULT_FONT_SIZE = 24

    # Required Interface Methods ##############

    def init(self):
        """
        This is a deferred-constructor of sorts.

        We don't do this work in `__init__` since we have less control
        over when the object is created than when we actually want to do
        the platform-specific initialization.

        For example, by the point this is called, we need to have called
        `pygame.init()`, but that would require us know that, and only construct
        the object after it was called, ex:

        # this would break
        engine = PygameDrawEngine()
        pygame.init()

        # this would work
        pygame.init()
        engine = PygameDrawEngine()

        This isn't a perfect solution to that problem, but a fair compromise for now.
        """
        self.screen = pygame.display.set_mode((world.WIDTH, world.HEIGHT))
        self.buffer = pygame.Surface((world.WIDTH, world.HEIGHT), pygame.SRCALPHA)

        # TODO: depending on system these fonts often do not have all the
        # necessary characters, find 3 widely available fonts that do
        world.draw_engine.make_font("small", 16, "mono")
        world.draw_engine.make_font("medium", 24, "copperplate")
        world.draw_engine.make_font("large", 48, "papyrus")

    def render(self, background_color: Color, drawables: list["Doodle"]):
        self.buffer.fill((*background_color, 255))
        for d in sorted(drawables, key=lambda d: d._z_index):
            d.draw()
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()

    def circle_draw(self, c: "Circle"):
        pygame.draw.circle(self.buffer, c.rgba, c.world_vec, c.radius_val)

    def rect_draw(self, r: "Rectangle"):
        # TODO: make accessors
        rect = pygame.Rect(
            r.world_x - r._width / 2,
            r.world_y - r._height / 2,
            r._width,
            r._height,
        )
        pygame.draw.rect(self.buffer, r.rgba, rect)

    def line_draw(self, ll: "Line"):
        pygame.draw.aaline(self.buffer, ll.rgba, ll.world_vec, ll.end_vec)

    def text_render(self, text: str, font: str, color: Color) -> "TODO":
        """returns an intermediated RenderedText"""
        return font.render(text, True, color)

    def text_draw(self, txt: "Text"):
        # this is a tight coupling, intentionally left
        text_rect = txt._rendered.get_rect(center=txt.world_vec)
        self.buffer.blit(txt._rendered, text_rect)

    def make_font(self, name, size, font=None, bold=False, italic=False):
        """
        The way fonts work in most graphics libraries requires choosing a font
        size, as well as any variation (bold, italic) at the time of creation.

        It would be nice if we could allow individual Text objects vary these,
        but doing so would be much more complex or require significantly more
        memory.
        """
        if font is None:
            font = pygame.font.Font(None, size)
        else:
            path = pygame.font.match_font(font, bold=bold, italic=italic)
            font = pygame.font.Font(path, size)
        self._fonts[name] = font

    def get_font(self, name=None):
        """
        Load a font by name, if no name is given, use the default font.
        """
        if not name:
            # None -> default font
            # load on demand
            if None not in self._fonts:
                self._fonts[None] = pygame.font.Font(None, self.DEFAULT_FONT_SIZE)
            return self._fonts[None]
        else:
            return self._fonts[name]


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
    FPS = 60
    MS_PER_FRAME = 1000 / FPS

    _instance = None

    def __init__(self):
        # This logic forms the basis of a check for prior instances.
        # Code could be added here to explicitly disallow them.
        if self._instance is None:
            self._instance = self
        self._drawables = []
        self.background_color = Color.WHITE
        self.screen = None
        self.draw_engine = PygameDrawEngine()

    def init(self):
        """
        Delayed initialization, can't be run at start
        but must be run once.
        """
        if self.screen:
            raise ValueError("Can't initialize world twice!")
        pygame.init()
        self.clock = pygame.time.Clock()
        self._elapsed = 0
        self.draw_engine.init()

    def clear(self):
        self._drawables = []

    def add(self, drawable):
        self._drawables.append(drawable)

    def tick(self):
        for d in self._drawables:
            d.update()

    def update(self):
        """
        Update & draw world to screen.
        """
        # update
        self._elapsed += self.clock.tick(self.FPS)
        while self._elapsed > self.MS_PER_FRAME:
            self._elapsed -= self.MS_PER_FRAME
            self.tick()

        # rendering
        self.draw_engine.render(self.background_color, self._drawables)


# our singleton instance
world = World()
