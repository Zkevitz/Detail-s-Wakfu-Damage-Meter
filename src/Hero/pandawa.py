from Hero.spell import Spell
from Hero.hero import Hero
class PANDAWA(Hero):
    color = "#957317"
    breed = 12
    def __init__(self):
        self.spells = [Spell("Souffle Enflammé", "Feu"),
                        Spell("Coup Laiteux", "Feu"),
                        Spell("Tournée Générale", "Feu"),
                        Spell("Flasque Explosive", "Feu"),
                        Spell("Toilaitage", "Feu"),
                        Spell("Souffle Laiteux", "Eau"),
                        Spell("Nuage Laiteux", "Eau"),
                        Spell("Tekilait", "Eau"),
                        Spell("Vague de Lait", "Eau"),
                        Spell("Fontaine de Laiqueur", "Eau"),
                        Spell("Triple Karma Leet", "Terre"),
                        Spell("Six Roses", "Terre"),
                        Spell("Frappe Fût", "Terre"),
                        Spell("Lucha L'ambrée", "Terre"),
                        Spell("Blitzkriek", "Terre"),
                        Spell("Cyanose", "Neutre"),
                        Spell("Tonneau sans Fond", "Neutre"),
                        Spell("Happy Hour", "Neutre"),
                        Spell("Maître de l'Ivresse", "Neutre"),
                        ]
        Hero.__init__(self, "PANDAWA")
