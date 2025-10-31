from Hero.spell import Spell
from Hero.hero import Hero
class OUGINAK(Hero):
    color = "#C77C38"
    breed = 15
    def __init__(self):
        self.spells = [Spell("Croc-en-jambe", "Terre"),
                        Spell("Bastonnade", "Terre"),
                        Spell("Molosse", "Terre"),
                        Spell("Hachure", "Terre"),
                        Spell("Saccade", "Terre"),
                        Spell("Emeute", "Eau"),
                        Spell("Fléau", "Eau"),
                        Spell("Rupture", "Eau"),
                        Spell("Plombage", "Eau"),
                        Spell("Balafre", "Eau"),
                        Spell("Balayage", "Air"),
                        Spell("Contusion", "Air"),
                        Spell("Cador", "Air"),
                        Spell("Brise'Os", "Air"),
                        Spell("Baroud", "Air"),
                        Spell("Canine", "Neutre"),
                        Spell("Art Canin", "Neutre"),
                        Spell("Force sage", "Neutre"),
                        Spell("Digestion", "Neutre"),
                        Spell("Flair", "Neutre"),
                        Spell("Fracture", "Air")]
        Hero.__init__(self, "OUGINAK")
