import sys
import copy
import random
import math
import pygame
import importlib
import typer
from .world import world


def main(modname: str):
    pygame.init()
    world.init()
    pygame.display.set_caption("Doodles")

    try:
        # try fully-qualified first
        mod = importlib.import_module(modname)
    except ImportError:
        # fall back to example
        try:
            mod = importlib.import_module("doodles.examples." + modname)
        except ImportError:
            raise ImportError(f"Tried to import {modname} and doodles.examples.{modname}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        world.render()
        pygame.display.flip()


if __name__ == "__main__":
    typer.run(main)
