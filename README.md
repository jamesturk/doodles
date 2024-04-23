# Doodles

This is a library that lets you write short programs that draw images or animations.

The design goals are, in approximate order of importance:

* Demonstrate some design patterns & concepts.
* Provide an example of a library design.
* Have a learning tool that's somewhat fun to play with.

Notably absent from this list: "make a useful tool" and "demonstrate the *right* way to do things."

This library demonstrates *ways* to do things, there is almost never a single correct way.
Sometimes choices will be made to provide more interesting code to learn from, or a more fun API to use.

## Rationales

I will document the reason that certain decisions were made, particularly when they were not my first thought.

If any decisions are unclear, I consider that a bug, please file a corresponding GitHub issue.

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

## Design Patterns

TODO: flesh this out with more notes

A number of design patterns are utilized in this library.
I'm open to suggestions for more to add, especially where an interesting feature can demonstrate the utility.

### Factory 

TODO: No factory yet surprisingly, should be easy to add one to add shapes, but can consider other options.

### Prototype

The `Doodle` class (and an override in `Group`) demonstrate the utility of the Prototype pattern.

Letting these objects specify how they are copied makes the desired behavior possible, the utility of which can be seen in `examples/copies.py`.

This would often be done via the `__copy__/__deepcopy__` methods, but for simplicity as well as API compatibility this is done in `.copy()` here.

### Singleton

The `World` class is treated as a Singleton and contains notes on alternate implementations.

### Bridge / Strategy

TODO: the planned Renderer class will demonstrate these

### Composite

The Group class (along with Doodle) forms a composite.

### Command

The structure of the Doodle object is a command class.
It stores the information about the action to be performed encapsulated.
It's entire purpose is to provide arguments to a draw* method.

### Observer

TODO: room to implement, dynamic properties?

### Template Method

The update method, the draw method.

### Visitor

TODO: maybe use along with group?

### Flyweight Cache

Text's Font Cache is a flyweight
