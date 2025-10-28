from Hero.spell import Spell
from Hero.hero import Hero
class OUGINAK(Hero):
    color = "#FF0000"
    breed = 15
    def __init__(self):
        self.spells = []
        Hero.__init__(self, "OUGINAK")
