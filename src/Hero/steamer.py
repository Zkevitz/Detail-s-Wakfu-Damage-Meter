from Hero.spell import Spell
from Hero.hero import Hero
class STEAMER(Hero):
    color = "#522C4C"
    breed = 16
    def __init__(self):
        self.spells = [Spell("Courant", "Eau"),
                        Spell("Ecume", "Eau"),
                        Spell("Évaporation", "Eau"),
                        Spell("Flibuste", "Eau"),
                        Spell("Dissolution", "Eau"),
                        Spell("Crache flammes", "Feu"),
                        Spell("Feu ardent", "Feu"),
                        Spell("Calcination", "Feu"),
                        Spell("Flambage", "Feu"),
                        Spell("Sabordage", "Feu"),
                        Spell("À la masse", "Terre"),
                        Spell("Piétinement", "Terre"),
                        Spell("Pilonnage", "Terre"),
                        Spell("Marteau aimant", "Terre"),
                        Spell("Choc", "Terre"),
                        Spell("Blindage", "Neutre"),
                        Spell("Tir de destruction", "Neutre"),
                        Spell("Tir de distance", "Neutre"),
                        Spell("Tir d'alignement", "Neutre"),
                        Spell("Surtension", "Neutre"),
                        Spell("Stratégie robotique", "Neutre"),
                        Spell("Roues chaudes", "Neutre") # a verifier 
                        ]
        Hero.__init__(self, "STEAMER")