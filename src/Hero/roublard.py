from Hero.spell import Spell
from Hero.hero import Hero
class ROUBLARD(Hero):
    color = "#FF0000"
    breed = 13
    def __init__(self):
        self.spells = []
        Hero.__init__(self, "ROUBLARD")
