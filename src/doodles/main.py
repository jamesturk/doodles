"""
Entrypoint for running doodles.

Understanding this module is not important to undertanding
the architecture.

The most interesting thing here is that it dynamically loads
a module based on name, using `importlib`.

This file also currently contains a hard dependency on pygame,
it probably makes sense to factor this out too so that the
underlying library is swappable, not just the drawing code.
"""
import sys
from pathlib import Path
import pygame
import importlib
import typer
from .world import world


def get_examples() -> list[str]:
    """
    Looks in the doodles/examples directory and gets a list of modules.
    """
    module_path = Path(__file__).parent / "examples"
    submodules = [
        file.stem for file in module_path.glob("*.py") if file.name != "__init__.py"
    ]
    return submodules


def load_module(modname: str):
    """
    Loads a module by name (either by absolute path or from within
    examples).

    Once loaded, the module's `create()` function is called, which should
    create instances of all drawable objects.
    """
    pygame.display.set_caption("doodles: " + modname)
    world.clear()
    try:
        # try fully-qualified first
        mod = importlib.import_module(modname)
    except ImportError:
        # fall back to example
        try:
            mod = importlib.import_module("doodles.examples." + modname)
        except ImportError:
            raise ImportError(
                f"Tried to import {modname} and doodles.examples.{modname}"
            )
    return mod.create()


def main(modname: str = None):
    """
    Entrypoint method.

    Loads a module then runs the core app loop.
    """

    # initalize world and underlying frameworks
    world.init()

    # get list of all examples and load first one if no name given
    examples = get_examples()
    ex_index = 0
    if modname:
        load_module(modname)
    else:
        load_module(examples[ex_index])

    # run until the application is quit
    while True:

        # this is a pygame event loop, it monitors which keys are pressed
        # and changes the example if left/right are pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    ex_index = (ex_index + 1) % len(examples)
                    load_module(examples[ex_index])
                elif event.key == pygame.K_LEFT:
                    ex_index = (ex_index - 1) % len(examples)
                    load_module(examples[ex_index])

        # update the world animations and draw
        world.update()


if __name__ == "__main__":
    typer.run(main)
