from doodles import Circle, Color
import random
from doodles.world import world

"""
Demonstrates two different update strategies.

This uses the Template Method pattern, by implementing update
the behavior of an object can be overriden.

Sometimes a default method would be supplied, but just as often
it is left as a pass-through like we see here.

Objects without an update method are static.
"""


class Ball(Circle):
    def __init__(self):
        super().__init__()
        self.speed = 9 + random.random() * 5

    def update(self):
        self.move(0, self.speed)
        if self.world_y > world.HEIGHT + 20:
            self.move(0, -world.HEIGHT - 20)


class GravityBall(Circle):
    def __init__(self):
        super().__init__()
        self.accel = 0.5  # accel per frame
        self.speed = random.random() * 10

    def update(self):
        self.speed += self.accel
        self.move(0, self.speed)
        if self.world_y > world.HEIGHT - 10:
            self.speed *= -0.98  # dampening
            self.y(world.HEIGHT - 10.01)


def create():
    [Ball().pos(40 * i, 0).radius(10).color(Color.BLUE) for i in range(21)]
    [
        GravityBall().pos(20 + 40 * i, 0).radius(10).color(Color.PURPLE)
        for i in range(21)
    ]
