"""
This file exposes the "public interface" for the library.

While you've often dealt with blank __init__ files, this is
making explicit which classes and functions are meant
to be used outside of the library.

Importing these here means a user can import these as

"from doodle import Line" instead of "from doodle.lines import Line"

This means the library author(s) can move around the implementation
as they wish without disrupting users.

For small libraries, it makes sense for a single __init__ to do this,
whereas for larger libraries like Django it is not common to require
users to import the specific portions they're using. (Though even
then there are public/non-public files.)
"""
from .doodles import Doodle, Group
from .lines import Line
from .shapes import Circle, Rectangle
from .color import Color
from .text import Text


__all__ = ["Doodle", "Group", "Line", "Circle", "Rectangle", "Color", "Text"]
