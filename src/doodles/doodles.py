"""
This module defines the base interface that all Doodle objects
will need to implement.

It defines two classes: Doodle and Group.

Their docstrings will give specific detail, but the implementations
are closely linked, as a Group is both a type of Doodle and contains
a collection of additional Doodle-derived classes.

This is a reasonable example of when two classes might reasonable share a file.
"""
import random
import copy
import time
from abc import ABC, abstractmethod
from typing import Callable, Self, Any
from .color import Color
from .world import world

UpdateCallable = Callable[[float], Any]

class Doodle(ABC):
    """
    A doodle is a set of drawing primitives.

    Each doodle has a position and a color.
    Default: (0, 0) & black

    Additionally a doodle can have a parent,
    which forms the basis of a hierarchy between them.

    Doodles are drawn relative to their parent, so if a circle
    is placed at (100, 100) and has a child point placed at (10, 10)
    that point would appear ag (110, 110).

    Careful attention is paid in this inheritance hierarchy to the
    Liskov substitution principle.
    """

    # annotations for instance attributes
    _parent: Self | None
    _updates: list[tuple[str, UpdateCallable]]
    _color: tuple[int, int, int]
    _alpha: int
    _z_index: float

    def __init__(self, parent=None):
        # To avoid all child constructors having an ever-expanding
        # number of parameters as more customization options arrive,
        # the design decision was made
        # that at creation time, all Doodles will have defaults
        # positioned at (0, 0), black, opaque, etc.
        #
        # All child classes should follow this same guidance
        # setting a *visible* (i.e. non-zero) default.
        self._parent = parent
        self._updates = []
        self._color = parent._color if parent else Color.BLACK
        self._alpha = parent._alpha if parent else 255
        self._z_index = 0

        # Design Note:
        # Is storing this vector in a tuple the right thing to do?
        # It might make more sense to store _x and _y, or use
        # a library's optimized 2D vector implementation.
        #
        # All references to _pos_vec are internal to the class,
        # so it will be trivial to swap this out later.
        self._pos_vec = (0, 0)

        self._register()

    def _register(self):
        """
        This private method ensures that the parent
        knows about the child object.

        It also registers every drawable object with the
        World singleton (see world.py) which ensures that
        it is drawn.
        """
        if self._parent:
            self._parent.add(self)
        world.add(self)

    @abstractmethod
    def draw(self) -> None:
        """
        All doodles need to be drawable, but there is no
        way we can provide an implementation without
        knowing more about a concrete shape (Circle, Line, etc.)

        We define this interface, and mark it abstract so that
        derived classes will be forced to conform to it.
        """
        pass

    def copy(self) -> Self:
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

    # animate #######################

    def animate(self, prop_name: str, update_func: UpdateCallable) -> Self:
        self._updates.append((prop_name, update_func))
        return self

    def update(self) -> None:
        """
        Default implementation is to support
        update function behavior.

        Can be overriden (see examples.balls)
        to provide per-object update behavior.
        """
        cur_time = time.time()

        for prop, anim_func in self._updates:
            # attributes on Doodle are set via setter functions
            # prop is the name of a setter function, which we
            # retrieve here, and then populate with the result
            # of anim_func(time)
            setter = getattr(self, prop)
            new_val = anim_func(cur_time)
            setter(new_val)

    # Setters #######################

    # As noted in the design documentation, the decision
    # was made to have setters be the name of the attribute.
    #
    # These modify & return the object.
    #
    # All setters (and modifiers) must return self.

    def color(self, color: tuple[int, int, int]) -> Self:
        """
        Color works as a kind of setter function.

        The only unique part is that it returns self, accomodating the
        chained object pattern.
        """
        self._color = color
        return self

    def pos(self, x: float, y: float) -> Self:
        """
        Another setter, just like color.

        As noted above, this encapsulates our storage decision for our 2D vector.
        """
        self._pos_vec = (x, y)
        return self

    def x(self, x: float) -> Self:
        """
        Setter for x component.
        """
        self._pos_vec = (x, self._pos_vec[1])
        return self

    def y(self, y: float) -> Self:
        """
        Setter for x component.
        """
        self._pos_vec = (self._pos_vec[0], y)
        return self

    def alpha(self, a: int) -> Self:
        """
        Setter for alpha transparency
        """
        self._alpha = a
        return self

    def z(self, z: float) -> Self:
        """
        Setter for z_index
        """
        self._z_index = z
        return self

    # Modifiers #################

    # These modify properties like setters, but allow
    # multiple operations to be done in a single call.
    #
    # They can also take advantage of knowledge of current
    # state, like `move` which applies a delta to the position.

    def move(self, dx: float, dy: float) -> Self:
        """
        This shifts the vector by a set amount.

        By calling self.pos() instead of setting the vector again
        here it will make use of any future validation logic added to that
        function.
        """
        return self.pos(self._pos_vec[0] + dx, self._pos_vec[1] + dy)

    def random(self) -> Self:
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

    # Getters ################

    @property
    def world_x(self) -> float:
        """
        A read-only attribute "doodle.world_x" that will
        return the screen position derived from the parent position
        plus the current object's x component.

        If a parent object is at (100, 100) and the child is at (10, 10)
        that should come through as (110, 110) in world coordinates.

        Note the recursion here, parent.world_x is an instance of doodle.world_x.

        For another example:

        A x = 100
        |--------B x = 10
                 |--------C.world_x 20

        When drawing object C, world_x will call B.world_x which will call
        A.world_x.
        B will return 110, and C therefore returns 130.
        """
        if self._parent:
            return self._parent.world_x + self._pos_vec[0]
        return self._pos_vec[0]

    @property
    def world_y(self) -> float:
        """
        See documentation for .world_y above.
        """
        if self._parent:
            return self._parent.world_y + self._pos_vec[1]
        return self._pos_vec[1]

    @property
    def world_vec(self) -> tuple[float, float]:
        """
        Obtain derived position vector as a 2-tuple.
        """
        return self.world_x, self.world_y

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """
        Access for color+alpha, used by draw functions
        which need a 4-tuple.
        """
        return (*self._color, self._alpha)


class Group(Doodle):
    """
    A concrete-in-implementation, abstract-in-concept doodle.

    A group is merely a list of other doodles, allowing
    doodles to be arranged/moved/updated in a tree-like manner.

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
        # Like all constructors derived from doodle, this constructor
        # initializes the parent Doodle class, and then adds its own
        # additional attributse.
        super().__init__(parent)
        self._doodles = []

    def __repr__(self):
        return f"Group(pos={self.world_vec}, doodles={len(self._doodles)})"

    def draw(self) -> None:
        """
        Groups, despite being an abstract concept, are drawable.
        To draw a group is to draw everything in it.

        This is done by default, since all drawables will be
        registered with the scene upon creation.

        Thus the *complete* implementation of this function
        is to "pass", the drawing will be handled by the child
        doodles.
        (If they weren't already registered with the world singleton
        this would loop over all child doodles and draw them).
        """
        pass

    def copy(self) -> Self:
        """
        An override of copy that handles the special
        case of having a mutable list of Doodles
        as an attribute.
        """
        # still a shallow copy of base data since
        # we're going to overwrite _doodles separately
        new = super().copy()
        new._doodles = []
        for child in self._doodles:
            # this code happens outside of Doodle.copy so that
            # the child is never accidentally registered with
            # the old parent
            child = copy.copy(child)
            child._parent = new
            child._register()
        return new

    def color(self, color: tuple[int, int, int]) -> Self:
        """
        An override of Doodle.color.

        What _color should do on Groups is a bit ambiguous.

        The way parent-child relationships work here means
        this color will never be used directly.
        Instead the decision was made that child objects
        will be colored by a call to this, and new
        children will be colored the color set on the parent
        group when added.

        Subsequent calls to color on child elements will recolor them
        allowing a group to have different colors within it.

        The position is handled differently (see world_x)
        since a moving parent should always move the children.
        """
        super().color(color)
        for d in self._doodles:
            d.color(color)
        return self

    def add(self, doodle: Doodle) -> Self:
        """
        The only unique method of this class, allowing us
        to add objects to the group.

        A simple implementation, but note that we set doodle._parent.

        This assignment is, strictly speaking, a violation of class
        boundaries. Sometimes two classes work together
        in a way that makes this necessary, as noted above.
        In some languages this would be done via a "protected"
        attribute, which is a status between public and private
        that only lets certain classes access internals.

        In Python, _parent is merely a suggestion,
        and in this case, it is a suggestion that we can safely
        ignore.

        These classes are tightly coupled to one another,
        hence their implementations living side-by-side and
        being allowed to peek at one another's internals.

        The alternative would be to have a set_parent() method
        but since we want groups to add children and not vice-versa
        there's no reason to add set_parent() to Doodle since
        it shouldn't be called by anything other than Group.

        So in effect, we're ensuring the encapsulation of Doodle's
        behavior everywhere else by breaking that rule here.
        """
        self._doodles.append(doodle)
        doodle._parent = self
        return self
