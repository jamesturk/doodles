from doodles.doodles import Group, Circle, Color
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
        self.speed = 0.005 + random.random() * 0.005

    def update(self):
        self.move(0, self.speed)
        if self.y > world.HEIGHT + 20:
            self.move(0, -world.HEIGHT-20)

balls = [Ball().pos(40*i, 0).radius(10).color(Color.BLUE) for i in range(21)]


class GravityBall(Circle):
    def __init__(self):
        super().__init__()
        self.accel = 0.0000001 # accel per frame
        self.speed = random.random() * 0.002

    def update(self):
        self.speed += self.accel
        self.move(0, self.speed)
        if self.y > world.HEIGHT - 10:
            self.speed *= -0.98 # dampening
            self.pos(self.x, world.HEIGHT - 10.01)


grav = [GravityBall().pos(20+40*i, 0).radius(10).color(Color.PURPLE) for i in range(21)]
