from Hero.spell import Spell
from Hero.hero import Hero
class HUPPERMAGE(Hero):
    color = "#C9A5A5"
    breed = 19
    def __init__(self):
        self.spells = [Spell("Halo Chatoyant", "Neutre")]
        Hero.__init__(self, "HUPPERMAGE")
