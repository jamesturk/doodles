import random
import copy
import math
import pygame
from abc import ABC, abstractmethod
from .color import Color
from .world import world


class Doodle(ABC):
    """
    A doodle is a set of drawing primitives.

    Each doodle has a position and a color.
    Default: (0, 0) & black

    Additionally a doodle can have a parent,
    which forms the basis of a hierarchy between them.

    Doodles are drawn relative to their parent, so if a circle
    is placed at (100, 100) and has a child point placed at (10, 10)
    that point would appear at (110, 110).

    Careful attention is paid in this inheritance hierarchy to the
    Liskov substitution principle.
    """

    def __init__(self, parent=None):
        self._parent = parent
        self._color = parent._color if parent else Color.BLACK
        self._z_index = 0
        # Is storing this vector in a tuple the right thing to do?
        # It might make more sense to store _x and _y, or use
        # a library's optimized 2D vector implementation.
        #
        # All references to _pos_vec are internal to the class,
        # so it will be trivial to swap this out later.
        self._pos_vec = (0, 0)
        if parent:
            # register with parent for updates
            self._parent.add(self)
        world.add(self)

    @abstractmethod
    def draw(self, screen) -> None:
        """
        All doodles need to be drawable, but there is no
        way we can provide an implementation without
        knowing more about a concrete shape (Circle, Line, etc.)

        We define this interface, and mark it abstract so that
        derived classes will be forced to conform to it.
        """
        pass

    def copy(self) -> "Doodle":
        """
        It will be useful to have the ability to obtain a copy
        of a given doodle to create repetitive designs.

        This method is provided to fit the chained-object pattern
        that will be used by the rest of the Doodle API.

        Additionally, while a shallow copy is enough for most
        cases, it will be possible for child classes to override
        this to opt for a deepcopy or other logic.
        """
        new = copy.copy(self)
        world.add(new)
        return new

    def color(self, r: int, g: int, b: int) -> "Doodle":
        """
        Color works as a kind of setter function.

        The only unique part is that it returns self, accomodating the
        chained object pattern.
        """
        self._color = (r, g, b)
        return self

    def pos(self, x: float, y: float) -> "Doodle":
        """
        Another setter, just like color.

        As noted above, this encapsulates our storage decision for our 2D vector.
        """
        self._pos_vec = (x, y)
        return self

    def z_index(self, z: float) -> "Doodle":
        """
        Setter for z_index
        """
        self._z_index = z
        return self

    def move(self, dx: float, dy: float) -> "Doodle":
        """
        This shifts the vector by a set amount.

        By calling self.pos() instead of setting the vector again
        here it will make use of any future validation logic added to that
        function.
        """
        return self.pos(self._pos_vec[0] + dx, self._pos_vec[1] + dy)

    def random(self) -> "Doodle":
        """
        Randomize the position and color.
        """
        x = random.random() * world.WIDTH
        y = random.random() * world.HEIGHT
        r, g, b = Color.random()
        # again here, we opt to use the setters so that
        # future extensions to their behavior will be
        # used by all downstream functions
        return self.pos(x, y).color(r, g, b)

    @property
    def x(self) -> float:
        """
        A read-only attribute "doodle.x" that will
        return the screen position derived from the parent position
        plus the current object's x component.

        Note the recursion here, parent.x is an instance of doodle.x.

        For example:

        A.x = 100
        |--------B.x 10
                 |--------C.x 20

        When drawing object C, parent.x will call B.x, which will call A.x.
        B.x will return 110, and C.x will therefore return 130.
        """
        if self._parent:
            return self._parent.x + self._pos_vec[0]
        return self._pos_vec[0]

    @property
    def y(self) -> float:
        """
        See documentation for .x above.
        """
        if self._parent:
            return self._parent.y + self._pos_vec[1]
        return self._pos_vec[1]

    # @property
    # def z_index(self) -> float:
    #     return self._z_index

    @property
    def pos_vec(self) -> (float, float):
        """
        Obtain derived position vector as a 2-tuple.
        """
        return self.x, self.y


class Line(Doodle):
    def __init__(self, parent=None):
        """
        We keep the same interface as Doodle, to follow the Liskov substitution
        principle.

        We could add more *optional* arguments, but no more required ones
        than the parent class.
        """
        super().__init__(parent)
        # a line is stored as a position (on the parent class)
        # and an offset vector
        self._offset_vec = (10, 0)

    def __repr__(self):
        return f"Line(pos={self.pos_vec}, end={self.end_vec}, {self._color})"

    def draw(self, screen):
        """
        Implementation of the abstract draw function for the line.

        Note: This is a classic violation of single responsibility.

        Instead, you could imagine a class like:

        class DrawingBackend:
            def draw_doodle(doodle_type, doodle): ...

        class PygameBackend(DrawingBackend):
            def draw_line(...): ...

        This would make it possible to attach different
        drawing backends, restoring single-responsibility
        to the class and gaining flexibility from separating
        presentation logic from data manipulation.
        """
        pygame.draw.line(screen, self._color, self.pos_vec, self.end_vec)

    def to(self, x: float, y: float) -> "Doodle":
        """
        A setter for the line's offset vector.

        Example usage:

        Line().pos(10, 10).to(50, 50)

        Makes a line from (10, 10) to (50, 50).
        """
        self._offset_vec = (x, y)
        return self

    def vec(self, degrees: float, magnitude: float):
        """
        Alternate constructor, to create offset vector from angle & length.
        """
        return self.to(
            magnitude * math.cos(math.radians(degrees)),
            magnitude * math.sin(math.radians(degrees)),
        )

    def random(self) -> "Doodle":
        """
        Overrides the parent's random, by extending the behavior.

        This is an example of the open/closed principle.
        We aren't modifying the parent classes' random function
        since doing so would be fragile and break if the
        parent class added more options.

        Instead we just call it, and extend it with additional
        randomization.
        """
        super().random()
        magnitude = random.random() * 100
        degrees = random.random() * 360
        return self.vec(degrees, magnitude)

    @property
    def end_vec(self):
        """
        Parallel to pos_vec for end of line.
        """
        return (
            self.x + self._offset_vec[0],
            self.y + self._offset_vec[1],
        )


class Group(Doodle):
    """
    For now, only Group objects can have child doodles.
    It may be desirable to let any object serve as a parent
    but for now, groups are needed.
    (This is analagous to files & directories making up a tree hierarchy.)

    This is an example of a design that requires cooperation between
    two classes.
    Each Doodle needs a _parent reference, which should only ever
    be a Group.
    In turn, each Group has a list of _doodles.

    This design is possible in Python due to light type coupling, but
    in some languages would be much trickier to pull off.
    """

    def __init__(self):
        super().__init__()
        self._doodles = []

    def draw(self, screen):
        """
        Groups, despite being an abstract concept, are drawable.
        To draw a group is to draw everything in it.

        This is done by default, since all drawables will be
        registered with the scene upon creation.
        """
        pass

    def copy(self) -> "Group":
        """
        An override.

        We are storing a list, so deep copies are necessary.
        """
        new = copy.deepcopy(self)
        world.add(new)
        return new

    def color(self, r: int, g: int, b: int) -> "Doodle":
        """
        Another override.

        Nothing will ever be drawn in the parent
        color, but we do want to have the set
        cascade down to child objects.

        We don't cascade pos() calls, why not?
        """
        super().color(r, g, b)
        for d in self._doodles:
            d.color(r, g, b)
        return self

    def add(self, doodle: "Doodle") -> "Group":
        """
        The only unique method of this class, allowing us
        to add objects to the group.

        Note the violation of class boundaries here.
        """
        self._doodles.append(doodle)
        doodle._parent = self
        # This assignment is, strictly speaking, a violation of class
        # boundaries. Sometimes two classes work together
        # in a way that makes this necessary, as noted above.
        # In some languages this would be done via a "protected"
        # attribute, which is a status between public and private
        # that only lets certain classes access internals.
        #
        # In Python, _parent is merely a suggestion,
        # and since it is likely that the same author wrote both
        # classes, it is a suggestion that we can safely ignore
        # if we understand the implications of tightly
        # binding the implementations of these two classes.
        return self


class Circle(Doodle):
    def __init__(self, parent=None):
        """
        This is a less interesting class than Line, but very similar.
        """
        super().__init__(parent)
        # circle is a position & radius
        self._radius = 0

    def __repr__(self):
        return f"Circle(pos={self.pos_vec}, radius={self._radius}, {self._color})"

    def draw(self, screen):
        pygame.draw.circle(screen, self._color, self.pos_vec, self._radius)

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
        return self.radius(random.random*90 + 10)
