from Hero.spell import Spell
from Hero.hero import Hero
class FECA(Hero):
    color = "#CCCC00"
    breed = 1
    def __init__(self):
        self.spells = [Spell("Fécalistofedes", "Feu"),
                        Spell("Météorite", "Feu"),
                        Spell("Attaque naturelle", "Feu"),
                        Spell("Magma", "Feu"),
                        Spell("Volcan", "Feu"),
                        Spell("Goutte", "Eau"),
                        Spell("Onde", "Eau"),
                        Spell("Avalanche", "Eau"),
                        Spell("Orage", "Eau"),
                        Spell("Lame de fond", "Eau"),
                        Spell("Frappe tellurique", "Terre"),
                        Spell("Orbe défensif", "Terre"),
                        Spell("Bastion", "Terre"),
                        Spell("Rempart", "Terre"),
                        Spell("Bâton", "Terre"),
                        #Spell("Assurance tous risques", "Neutre"),
                        #Spell("Uppercut", "Neutre"),
                        #Spell("Éventrail", "Neutre"),
                        ]
        Hero.__init__(self, "FECA")
