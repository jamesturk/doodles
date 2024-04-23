import random
import itertools
from doodles import Group, Circle, Color, Text

# TODO: depending on system these fonts often do not have all the
# necessary characters, find 3 widely available fonts that do
Text.make_font("small", 16, "mono")
Text.make_font("medium", 24, "copperplate")
Text.make_font("large", 48, "papyrus")

# Via ChatGPT
hello_world = [
    "Hello, World!",  # English
    "Hola, Mundo!",  # Spanish
    "Bonjour, Monde!",  # French
    "Hallo, Welt!",  # German
    "Ciao, Mondo!",  # Italian
    "こんにちは、世界！",  # Japanese
    "안녕하세요, 세계!",  # Korean
    "Привет, мир!",  # Russian
    "Olá, Mundo!",  # Portuguese
    "नमस्ते, दुनिया!",  # Hindi
    "Merhaba, Dünya!",  # Turkish
    "Salam, Dünya!",  # Azerbaijani
    "Hej, Världen!",  # Swedish
    "Hei, Maailma!",  # Finnish
    "שלום, עולם!",  # Hebrew
    "Szia, Világ!",  # Hungarian
    "Zdravo, Svijete!",  # Bosnian
    "Sawubona, Mhlaba!",  # Zulu
    "Marhaba, Alalam!",  # Arabic
    "你好，世界！",  # Mandarin Chinese
]


def create():
    # use a generator to include each one 3x
    for greeting in itertools.chain.from_iterable(itertools.repeat(hello_world, 3)):
        Text().random().font(
            random.choice(("small", "medium", "large"))
        ).color(random.choice((Color.LIGHT_GREY, Color.DARK_GREY))).text(greeting)
