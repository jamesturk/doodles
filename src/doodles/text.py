"""
This is the most complicated Doodle-derived class.

Like shapes, the interface is mostly identical to Line.
If you are mainly trying to understand the interfaces it is
safe to skip this one.

There is some more complexity here because fonts need to be
pre-rendered. This means that when `text` is called, an internal
cached copy of the font already drawn to a temporary piece of memory
"surface" in graphics programming parlance.

This is an example of a type of class where when a property changes
some additional computation can be done to precompute/cache
some expensive logic.

Look at _render() for more.
"""
from .doodles import Doodle
from .world import world


class Text(Doodle):
    def __init__(self, parent=None):
        """
        A text object stores a reference to a pre-loaded font,
        the text to be drawn, and an internal `_rendered` object
        that *can* be used to store the cached text.

        Not all implementations will require pre-rendering, but
        Pygame (the first implementation) does, so it is necessary
        for the interface as written here.

        When drawn, text will be centered at `pos`
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

        Text needs to be rendered once on change to be performant.
        Doing this in draw would be much slower since it is called
        much more often than the text changes.

        (draw called ~60 times per second, _render only called when
         text is updated.)
        """
        if not self._font:
            self._font = world.draw_engine.get_font()  # default font
        self._rendered = world.draw_engine.text_render(
            self._text, self._font, self._color
        )

    def font(self, font: str) -> "Doodle":
        self._font = world.draw_engine.get_font(font)
        return self
