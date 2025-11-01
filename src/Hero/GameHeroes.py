from Hero.iop import IOP
from Hero.cra import CRA
from Hero.zobal import ZOBAL
from Hero.eniripsa import ENIRIPSA
from Hero.xelor import XELOR
from Hero.sacrieur import SACRIEUR
from Hero.enutrof import ENUTROF
from Hero.feca import FECA
from Hero.steamer import STEAMER
from Hero.osamodas import OSAMODAS
from Hero.pandawa import PANDAWA
from Hero.ecaflip import ECAFLIP
from Hero.sadida import SADIDA
from Hero.roublard import ROUBLARD
from Hero.ouginak import OUGINAK
from Hero.eliotrope import ELIOTROPE
from Hero.huppermage import HUPPERMAGE
from Hero.sram import SRAM
from Hero.Ennemy import Ennemy
from Hero.invo import Invo
import random
import re
import logging
from core.utils import isControlledByAI
logger = logging.getLogger(__name__)
iop = IOP()
cra = CRA()
osamodas = OSAMODAS()
eniripsa = ENIRIPSA()
xelor = XELOR()
enutrof = ENUTROF()
sacrieur = SACRIEUR()
zobal = ZOBAL()
steamer = STEAMER()
pandawa = PANDAWA()
sadida = SADIDA()
feca = FECA()
ecaflip = ECAFLIP()
sram = SRAM()
roublard = ROUBLARD()
ouginak = OUGINAK()
eliotrope = ELIOTROPE()
huppermage = HUPPERMAGE()
actualFight = None
GameHeroes = [iop, cra, eniripsa, xelor, enutrof, sacrieur, zobal,
             feca, steamer, pandawa, ecaflip, sadida, sram, roublard,
              ouginak, eliotrope, huppermage, osamodas]
EnnemyList = []

def handleNewFight():
    from core.calc import PlayedHeroes
    from core.interface_support import resetListbox
    if PlayedHeroes:
        for hero in PlayedHeroes :
            hero.InvocList.clear()
            hero.clear()
        PlayedHeroes.clear()
    if EnnemyList:
        EnnemyList.clear()
    PlayedHeroes = []
    resetListbox()
    global actualFight
    actualFight = random.randint(1000, 99999)

def GenerateRapport():
    from core.calc import PlayedHeroes
    from core.extractData import extractData
    extractData(PlayedHeroes, EnnemyList)

def handleInvoc(line):
    from core.calc import PlayedHeroes
    match = re.search(r"\[Information \(combat\)\]\s+([^:]+):\s+Invoque un", line)
    InvocName = re.search(r"Invoque un(?:\(e\))?\s+([A-Za-zÀ-ÖØ-öø-ÿ'`\- ]+)", line)
    if match :
        matchName = match.group(1)
        for hero in PlayedHeroes :
            if hero.name == matchName :
                hero.InvocList.append(Invo(InvocName.group(1).strip()))
                logger.debug(f"{InvocName.group(1)} ?!=? {matchName}")
                if InvocName.group(1).strip() == "Lapino" :
                    logger.debug(f"Lapino invoquer auto ajout du Super Lapino")
                    hero.InvocList.append(Invo("Super Lapino"))
                elif InvocName.group(1).strip() == "Dark Lapino":
                    hero.InvocList.append(Invo("Super Dark Lapino"))
                break

def NewHero(line) :
    from core.calc import PlayedHeroes
    matchNumber = re.search(r"breed\s*:\s*(\d+)", line)
    fighter_name = re.search(r'fightId=[0-9]* (.*?) breed : ', line)
    id = re.search(r"breed\s*:\s*\d+\s*\[\s*(-?\d+)\s*\]", line)
    id = id.group(1)
    AI = isControlledByAI(line)
    fighter_name = fighter_name.group(1)
    if matchNumber :
        classNumber = int(matchNumber.group(1))
        if classNumber > 0 and classNumber <= 19 and AI == False:
            for hero in PlayedHeroes :
                logger.debug(f"Debug : {hero.name} =?!= {fighter_name}")
                if hero.name == fighter_name :
                    return
            for hero in GameHeroes :
                if hero.breed == classNumber :
                    hero.name = fighter_name
                    PlayedHeroes.append(hero)
        else :
            for Ennemies in EnnemyList :
                if Ennemies.id == id:
                    return
            EnnemyList.append(Ennemy(fighter_name, classNumber, id))
            #TO DO
