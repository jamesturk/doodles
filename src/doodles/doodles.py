import random
import copy
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
        self._updates = []
        # Is storing this vector in a tuple the right thing to do?
        # It might make more sense to store _x and _y, or use
        # a library's optimized 2D vector implementation.
        #
        # All references to _pos_vec are internal to the class,
        # so it will be trivial to swap this out later.
        self._pos_vec = (0, 0)
        self._register()

    def _register(self):
        """ register with parent and world """
        if self._parent:
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

    def register_update(self, method, *args):
        self._updates.append((method, args))

    def update(self) -> None:
        """
        Default implementation is to support
        update function behavior.

        Can be overriden (see examples.balls)
        to provide per-object update behavior.
        """
        for method, args in self._updates:
            evaled_args = [arg() for arg in args]
            method(*evaled_args)

    def copy(self) -> "Doodle":
        """
        It will be useful to have the ability to obtain a copy
        of a given doodle to create repetitive designs.

        This method is provided to fit the chained-object pattern
        that will be used by the rest of the Doodle API.

        Additionally, while a shallow copy is enough for most
        cases, it will be possible for child classes to override
        this.
        """
        new = copy.copy(self)
        new._register()
        return new

    def color(self, color: tuple[int, int, int]) -> "Doodle":
        """
        Color works as a kind of setter function.

        The only unique part is that it returns self, accomodating the
        chained object pattern.
        """
        self._color = color
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
        color = Color.random()
        # again here, we opt to use the setters so that
        # future extensions to their behavior will be
        # used by all downstream functions
        return self.pos(x, y).color(color)

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

    def __init__(self, parent=None):
        super().__init__(parent)
        self._doodles = []

    def __repr__(self):
        return f"Group(pos={self.pos_vec}, doodles={len(self._doodles)})"

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
        new = copy.copy(self)
        new._register()
        new._doodles = []
        for child in self._doodles:
            child = copy.copy(child)
            child._parent = new
            child._register()
        return new

    def color(self, color: tuple[int, int, int]) -> "Doodle":
        """
        Another override.

        Nothing will ever be drawn in the parent
        color, but we do want to have the set
        cascade down to child objects.

        We don't cascade pos() calls, why not?
        """
        super().color(color)
        for d in self._doodles:
            d.color(color)
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
