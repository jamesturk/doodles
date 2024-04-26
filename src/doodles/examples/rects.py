from doodles import Rectangle, Color

def create():
    for _ in range(25):
        Rectangle().random(200).color(Color.BLACK).z(10)
        Rectangle().random(150).color(Color.DARK_BLUE).z(15)
        Rectangle().random(100).color(Color.DARK_GREY).z(20)
        Rectangle().random(50).color(Color.LIGHT_GREY).z(30)
