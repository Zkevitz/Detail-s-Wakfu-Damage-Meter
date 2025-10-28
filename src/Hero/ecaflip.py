from Hero.spell import Spell
from Hero.hero import Hero
class ECAFLIP(Hero):
    color = "#FF99FF"
    breed = 6
    def __init__(self):
        self.spells = [Spell("Roulette à dés", "Feu"),
                        Spell("Crapst", "Feu"),
                        Spell("Dé du chateux", "Feu"),
                        Spell("Dé six", "Feu"),
                        Spell("Feulement", "Feu"),
                        Spell("Langue rapeusee", "Eau"),
                        Spell("Lacérations", "Eau"),
                        Spell("Capucine", "Eau"),
                        Spell("Bas les pattes", "Eau"),
                        Spell("Pupuce", "Eau"),
                        Spell("Pile ou face", "Terre"),
                        Spell("All in", "Terre"),
                        Spell("Tout ou rien", "Terre"),
                        Spell("Trois cartes", "Terre"),
                        Spell("Bataille", "Terre"),
                        Spell("Black Jack", "Neutre"),
                        Spell("Topkaj", "Neutre"), #ajouter valeur par defaut
                        Spell("Félintuition", "Neutre"),
                        Spell("Le Chacrifice", "Neutre"),
                        Spell("Légère chance", "Neutre"),
                        Spell("Pile, je gagne", "Neutre"),
                        Spell("Légère malchance", "Neutre"),
                        Spell("Malchance", "Neutre"),
                        Spell("Légère chance", "Neutre"),
                        Spell("Le Destin d'Ecaflip", "Neutre"),
                        Spell("Chance", "Neutre")
                        #coup du sort vol de vie 
                        ]
        Hero.__init__(self, "ECAFLIP")


# PASSIF PUCIF INRECONNAISABLE