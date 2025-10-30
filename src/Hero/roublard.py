from Hero.spell import Spell
from Hero.hero import Hero
class ROUBLARD(Hero):
    color = "#3B3636"
    breed = 13
    def __init__(self):
        self.spells = [Spell("Barbrûlé", "Feu"),
                        Spell("Bombe collante", "Feu"),
                        Spell("Exécution", "Feu"),
                        Spell("Croisement", "Feu"),
                        Spell("Perforation", "Feu"),
                        Spell("Mitraille", "Terre"),
                        Spell("Tromblon", "Terre"),
                        Spell("Dague boomerang", "Terre"),
                        Spell("Pulsar", "Terre"),
                        Spell("Balle plombante", "Terre"),
                        Spell("Coup rapide", "Air"),
                        Spell("Tricherie", "Air"),
                        Spell("Bombe immolante", "Feu"),
                        Spell("Bombe paralysante", "Terre"),
                        Spell("Bombe aveuglante", "Air"),
                        Spell("Espingole", "Air"),
                        Spell("Fourbe lame", "Air"),
                        Spell("Oblitération", "Air"),
                        Spell("Fugitif", "Neutre"),
                        Spell("Tétanos", "Neutre"),
                        Spell("Fugitif", "Neutre"),]
        Hero.__init__(self, "ROUBLARD")
