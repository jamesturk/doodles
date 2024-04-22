import sys
from pathlib import Path
import pygame
import importlib
import typer
from .world import world

FPS = 60
MS_PER_FRAME = 1000 / 60


def get_examples():
    module_path = Path(__file__).parent / "examples"
    submodules = [
        file.stem for file in module_path.glob("*.py") if file.name != "__init__.py"
    ]
    return submodules

def load_module(modname):
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
    pygame.init()
    world.init()

    examples = get_examples()
    ex_index = 0
    if modname:
        load_module(modname)
    else:
        load_module(examples[ex_index])

    elapsed = 0
    clock = pygame.time.Clock()

    while True:
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
        elapsed += clock.tick(FPS)
        while elapsed > MS_PER_FRAME:
            elapsed -= MS_PER_FRAME
            world.tick()
        world.render()
        #print(clock.get_fps())
        pygame.display.flip()


if __name__ == "__main__":
    typer.run(main)
