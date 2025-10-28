from Hero.spell import Spell
from Hero.hero import Hero
class HUPPERMAGE(Hero):
    color = "#FF0000"
    breed = 18
    def __init__(self):
        self.spells = []
        Hero.__init__(self, "HUPPERMAGE")
