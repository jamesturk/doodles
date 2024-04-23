from doodles import Rectangle, Color, world
import random

def create():
    for _ in range(25):
        Rectangle().random(200).color(Color.BLACK).z_index(10)
        Rectangle().random(150).color(Color.DARK_BLUE).z_index(15)
        Rectangle().random(100).color(Color.DARK_GREY).z_index(20)
        Rectangle().random(50).color(Color.LIGHT_GREY).z_index(30)
        # Rectangle().random(250).color(
        #     random.choice((Color.BLACK, Color.LIGHT_GREY, Color.DARK_GREY, Color.WHITE))
        # )
