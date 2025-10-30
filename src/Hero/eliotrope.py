from Hero.spell import Spell
from Hero.hero import Hero
class ELIOTROPE(Hero):
    color = "#2BA0BD"
    breed = 18
    def __init__(self):
        self.spells = [Spell("Wakméha", "Eau"),
                        Spell("Pulsation", "Eau"),
                        Spell("Déluge", "Eau"),
                        Spell("Cataclysme", "Eau"),
                        Spell("Tourbillon", "Eau"),
                        Spell("Targe fracassante", "Terre"),
                        Spell("Heurt", "Terre"),
                        Spell("Raclée", "Terre"),
                        Spell("Egide ardente", "Terre"),
                        Spell("Séisme", "Terre"),
                        Spell("Flux torrentiel", "Air"),
                        Spell("Siphon", "Air"),
                        Spell("Salve éthérée", "Air"),
                        Spell("Tempête", "Air"),
                        Spell("Lame déchaînée", "Air"),
                        Spell("Cicatrisation", "Neutre"),
                        Spell("Bouclier de la fin", "Neutre"),]
        Hero.__init__(self, "ELIOTROPE")
