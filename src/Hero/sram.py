from Hero.spell import Spell
from Hero.hero import Hero
class SRAM(Hero):
    color = "#FF0000"
    breed = 4
    def __init__(self):
        self.spells = []
        Hero.__init__(self, "SRAM")
