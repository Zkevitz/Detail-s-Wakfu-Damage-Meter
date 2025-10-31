from Hero.spell import Spell
from Hero.hero import Hero
class SRAM(Hero):
    color = "#9E38C7"
    breed = 4
    def __init__(self):
        self.spells = [Spell("Piège de Lacération", "Feu"),
                        Spell("Piège de Silence", "Eau"),
                        Spell("Piège de Brume", "Air"),
                        Spell("Hémorragie", "Feu"),
                        Spell("Assassin", "Neutre")]
        Hero.__init__(self, "SRAM")
