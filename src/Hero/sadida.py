from Hero.spell import Spell
from Hero.hero import Hero
class SADIDA(Hero):
    color = "#FF99FF"
    breed = 10
    def __init__(self):
        self.spells = [Spell("Vaporiser", "Eau"),
                        Spell("Larme du Sadida", "Eau"),
                        Spell("Gadoule", "Eau"),
                        Spell("Rouille", "Eau"),
                        Spell("Drainage", "Eau"),
                        Spell("Ronce", "Terre"),
                        Spell("Engrais", "Terre"),
                        Spell("Herbes Folles", "Terre"),
                        Spell("Tremblement de Terre", "Terre"),
                        Spell("Ronces Multiples", "Terre"),
                        Spell("Bourrasque", "Air"),
                        Spell("Vent Empoisonné", "Air"),
                        Spell("Intoxiqué", "Air"),
                        Spell("Coup de Froid", "Air"),
                        Spell("Kohmir", "Air"),
                        Spell("Relent Boisé", "Air"),
                        Spell("Eveil Sylvestre", "Neutre"),
                        Spell("Toxines", "Neutre"),
                        Spell("Arbre", "Neutre"),
                        Spell("Tétatoxine", "Neutre"),
                        Spell("Maudit", "Air"),
                        Spell("Gonflage", "Eau"),
                        Spell("Egoulement", "Eau"),
                        Spell("Exploupée", "Neutre"),
                        Spell("Hydratée", "Eau"),
                        Spell("Prière Sadida", "Eau"),
                        Spell("Intoxiqué", "Air"),
                        Spell("Bistoufly", "Air"),
                        Spell("Fantoche", "Terre"),
                        ]
        Hero.__init__(self, "SADIDA")
