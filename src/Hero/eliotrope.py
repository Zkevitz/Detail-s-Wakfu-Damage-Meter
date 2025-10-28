from Hero.spell import Spell
from Hero.hero import Hero
class ELIOTROPE(Hero):
    color = "#FF0000"
    breed = 17
    def __init__(self):
        self.spells = []
        Hero.__init__(self, "ELIOTROPE")
