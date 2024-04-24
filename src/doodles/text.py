import pygame
from .doodles import Doodle
from .world import world


class Text(Doodle):
    def __init__(self, parent=None):
        """
        Text will be centered at `pos`
        """
        super().__init__(parent)
        self._text = ""
        self._rendered = None  # the surface we pre-render the text to
        self._font = None

    def __repr__(self):
        return f"Text(pos={self.pos_vec}, text={self._text}, parent={self._parent})"

    def draw(self):
        world.draw_engine.text_draw(self)

    def text(self, text: str) -> "Doodle":
        """
        A setter for the text.

        This is the only place text can change,
        so we can pre-render the surface here.
        """
        self._text = text
        self._render()
        return self

    def _render(self):
        """
        This function needs to set the _rendered property.

        _rendered may be relied upon by draw_engine.draw_text.
        """
        # text needs to be rendered once on change to be performant
        # doing this in draw would be much slower since it is called
        # much more often than the text changes
        if not self._font:
            self._font = world.draw_engine.get_font()  # default font
        self._rendered = world.draw_engine.text_render(
            self._text, self._font, self._color
        )

    def font(self, font: str) -> "Doodle":
        self._font = world.draw_engine.get_font(font)
        return self
