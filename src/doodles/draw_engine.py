import abc
from typing import TYPE_CHECKING

# this is needed because of circular references
if TYPE_CHECKING:
    from .colors import Color
    from .doodles import Doodle
    from .shapes import Rectangle, Circle
    from .lines import Line
    from .text import Text



class DrawEngine(abc.ABC):
    """
    This is an abstract class that defines the methods needed
    to have a drawing backend.

    This interface was *extracted* not designed.

    The first version of this library had a hard dependency on pygame
    for drawing.  Each shape had an overriden draw method that called
    pygame functions directly.

    The refactor in https://github.com/jamesturk/doodles/pull/1
    pulled this out by searching the code for all pygame references
    and extracting them into their own class. `PygameDrawEngine`.

    These are the signatures of that classes methods, so that
    a new implementation (to draw in OpenGL, or the browser, or on PDFs)
    could provide the necessary implementations of these functions.

    Note that starting with these as embedded and then extracting them
    is a perfectly valid way to get here, you could also be diligent
    while writing in the first place, and ensure that code needing
    isolation (such as a library you want to avoid tight coupling to)
    only is added to a specific class or module.
    """
    @abc.abstractmethod
    def init(self):
        """
        Called once, provides a place for the backend to initialize
        itself as needed.
        """

    @abc.abstractmethod
    def render(self, background_color: "Color", drawables: list["Doodle"]):
        """
        Workhorse function, should set background and then draw all Doodles.

        Will be called once per frame.
        """

    @abc.abstractmethod
    def circle_draw(self, circle: "Circle"):
        """
        Method to draw a Circle obj.
        """

    @abc.abstractmethod
    def rect_draw(self, rect: "Rectangle"):
        """
        Method to draw a Rectangle obj.
        """

    @abc.abstractmethod
    def line_draw(self, line: "Line"):
        """
        Method to draw a Line obj.
        """

    @abc.abstractmethod
    def text_render(self, text: "Text"):
        """
        Method to pre-render a text object.
        """

    @abc.abstractmethod
    def text_draw(self, text: "Text"):
        """
        Method to draw a pre-rendered text object.
        """

    # TODO: should make_font/get_font become part of the
    # reqwuired interface?
