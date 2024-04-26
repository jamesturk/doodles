# Doodles

This is a library that lets you write short programs that draw images or animations.

The design goals are, in approximate order of importance:

* Demonstrate some design patterns & concepts.
* Provide an example of a library design.
* Have a learning tool that's somewhat fun to play with.

Notably absent from this list: "make a useful tool" and "demonstrate the *right* way to do things."

This library demonstrates *ways* to do things, there is almost never a single correct way.
Sometimes choices will be made to provide more interesting code to learn from, or a more fun API to use.

## Running

Check this repo out locally, then:

```
poetry install
poetry run python -m doodles.main
```

Press left/right arrow to toggle through examples.

Feel free to modify the existing examples (`doodles/examples` or add your own).

## Architecture

TODO

## SOLID Principles

*Single Responsibility*

The most clear example of the single responsibility principle is that shapes do
not draw themselves.
This seems like a good idea, and indeed as I was drafting this they did, each shape
has a `draw` method that could draw itself.

Instead these methods dispatch to the currently active DrawEngine which contains
all drawing specific code.

This follows single responsibility, and gains a tangible benefit from it.

(See `lines.py draw` for a bit more discussion of this.)

*Open/Closed*

This principle asks that behaviors are extensible by inheritance,
not requiring modification to the base classes behavior.

The `Doodle.random()` method demonstrates this, the base random method
randomizes the properties common to all doodles (position, color).

Derived classes override this (see `Line.random()`, `Circle.random()`, etc.) by calling the base
implementation, and then adding their own random elements.

(See `lines.py random` for a bit more discussion of this.)

*Liskov Substitution*

Anywhere that the underlying code expects a `Drawable` it should be possible
to substitute any child class `Line`, `Rectangle`, etc.

This is ensured by having all of them define a common `draw` interface, and having
their constructors not take dozens of additional parameters. (See `Line.__init__`.)

*Interface Segregation*

This is largely given by counter-example, the principle here states that we must not force child classes to implement methods they do not use.

A counter-example to this would be if the pre-render, then draw dance that complicates the `Text` interface was extended to all types.

One could imagine having placed this logic at the `Doodle` class instead of `Line`.
That would mean that `Circle`, `Rectangle`, etc. would need to implement a (likely empty) method to fulfill this.

*Dependency Inversion*

Entities should depend on abstractions, not concrete implementations.

`World` depends on the `Doodle` interface (most explicitly through `draw`), but not on `Circle`, `Font`, etc.

This ensures adding new drawable `Doodles` only requires deriving a class, not modifying `World`.

## Design Patterns

A number of design patterns are utilized in this library.

I'm open to suggestions for more to add, especially where an interesting feature can demonstrate the utility.

### Prototype

<https://refactoring.guru/design-patterns/prototype>

The `Doodle` class (and override in `Group`) demonstrate the utility of the Prototype pattern.

Letting these objects specify how they are copied makes the desired behavior possible, the utility of which can be seen in `examples/copies.py`.

This would often be done via the `__copy__/__deepcopy__` methods, but for simplicity as well as API compatibility this is done in `.copy()` here.

### Singleton

<https://refactoring.guru/design-patterns/singleton>

The `World` class is treated as a Singleton and contains notes on alternate implementations.

### Strategy & Bridge

<https://refactoring.guru/design-patterns/strategy>

The interface created in `draw_engine.py` as well as implementation in `world.py` show the strategy pattern in action.

While this pattern can sometimes be achieved in a functional way by passing a function around, here the drawing strategy is more complex, and so gets aggregated into a class that allows swapping the entire strategy.

An alternate implementation of this class could draw to a PDF or web browser instead of Pygame window.

<https://refactoring.guru/design-patterns/bridge>

At the moment, the `World` and `PygameDrawEngine` are very tightly coupled,
this make sense because they both require `pygame`.

This creates a bridge pattern between the two, `World` handles update logic/the generic
form of drawing doodles, but the actual drawing is implemented in the draw engine.

### Composite

<https://refactoring.guru/design-patterns/composite>

This pattern allows objects to form a tree, usually by tracking child/parent relationships.

The `Group` class works closely with `Doodle` (both in `doodles.py`) to form a composite.

Groups of doodles can be moved/colored/etc. together by having the `Group` delegate method calls to the child elements.

Since `Group` is-a `Doodle`, groups of groups of groups can be created, allowing trees of any shape or size.

### Template Method

<https://refactoring.guru/design-patterns/template-method>

The core behavior of an object is implemented in the `Doodle` class which
has methods for positioning, coloring, etc.

The `update()` and `draw()` methods are templates, that if overriden, can
further refine the behavior

See `balls.py` for an example of the `update` method being used to demonstrate
the template method pattern.

### Command

<https://refactoring.guru/design-patterns/command>

The command pattern turns an intention into a packet of information about the
intended operation, so execution can be deferred.

Note that in all of the examples, the drawing does not happen when the object
is created, the creation of an object indicates that there will be some future
operation performed, based on the properties of the command class.

This allows our chained interface to work since

`Circle().move(20, 20).color(255, 0, 0)` does not immediately draw a circle when `move` is called, instead it is informing future draws to include that position. This avoids a non-red circle from being drawn, since the subsequent call to `color(255, 0, 0)` to
also run before the command is executed (via the `draw` method).

### Flyweight Cache

<https://refactoring.guru/design-patterns/flyweight>

Fonts need to be loaded once and are loaded in to shared memory
(currently in `PygameDrawEngine`) instead of having each `Text` object
load the same font.

This is done since it is common to use the same font multiple times in an
application, so having each text object load its own instance of a font would
be immensely wasteful.

This is the most complex part of the code currently, but you can see the logic in the font methods on the DrawEngine and you'll see it is mostly a dictionary mapping
parameters to created objects.

### Others

Some other patterns under consideration would be Observer, Factor, and Visitor.

All of these might have interesting applications in making art this way. (PRs welcome :))

## Rationales

A few more rationales for reason that certain decisions were made, particularly when they were not my first thought.

If any decisions elsewhere in the code are unclear and undocumented, I consider that a bug, please file a GitHub issue.

### Mutability

Often, an API based on chaining like this would be comprised of immutable objects.
Django's QuerySet mostly works in this way.

That was the original intention here as well, but once `Text` was added it was clear that it was going to be a lot more complex than it was worth.

`Text` requires an intermediate buffer to render the text to, and that buffer is then rendered to the screen. This would be incredibly expensive in a pure immutable approach, since there'd be no place to store that state.

The addition of state to the objects simplifies a lot of things, now when an object is created it can be registered with the `World`, if many intermediate copies were created in a chained call like `Circle().pos(100, 100).color(255, 0, 0).z(10).radius(4)` this approach would not be available to us.

### Naming Scheme

This library makes use of @property to create getters, but uses function chaining instead of property-based setters.

This complicates things a bit, since you can't write `self.x(100)` and use `self.x` as a property.

The unorthodox decision was made to use `x(100)` as a setter function, and use `.x_val` as the property name.

This is primarily because setting properties is more common than getting properties in doodles.
