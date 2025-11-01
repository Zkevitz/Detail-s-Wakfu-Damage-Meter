from Hero.spell import Spell
from Hero.hero import Hero
class OSAMODAS(Hero):
    color = "#FF0000"
    breed = 2
    def __init__(self):
        self.spells = [Spell("Aura lunaire", "Neutre"),
                        Spell("Aura Solaire", "Neutre")]
        Hero.__init__(self, "OSAMODAS")
