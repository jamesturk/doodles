import pygame
from .doodles import Doodle

# TOOD: make configurable
DEFAULT_FONT_SIZE = 24

class Text(Doodle):
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

    # this method is attached to the class `Text`, not individual instances
    # like normal methods (which take self as their implicit parameter)
    @classmethod
    def make_font(cls, name, size, font=None, bold=False, italic=False):
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
        cls._fonts[name] = font

    @classmethod
    def get_font(cls, name=None):
        if not name:
            # None -> default font
            # load on demand
            if None not in cls._fonts:
                cls._fonts[None] = pygame.font.Font(None, DEFAULT_FONT_SIZE)
            return cls._fonts[None]
        else:
            return cls._fonts[name]

    def __init__(self, parent=None):
        """
        Text will be centered at `pos`
        """
        super().__init__(parent)
        self._text = ""
        self._rendered = None
        self._font = None

    def __repr__(self):
        return f"Text(pos={self.pos_vec}, text={self._text}, parent={self._parent})"

    def draw(self, screen):
        text_rect = self._rendered.get_rect(center=(self.x, self.y))
        screen.blit(self._rendered, text_rect)

    def text(self, text: str) -> "Doodle":
        """
        A setter for the text
        """
        self._text = text
        # text needs to be rendered once on change to be performant
        # doing this in draw would be much slower since it is called
        # much more often than the text changes
        if not self._font:
            self._font = self.get_font()    # default font
        self._rendered = self._font.render(self._text, True, self._color)
        return self

    def font(self, font: str) -> "Doodle":
        # TODO: error checking
        self._font =  self._fonts[font]
        return self
