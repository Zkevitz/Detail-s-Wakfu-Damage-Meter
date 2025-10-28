from Hero.iop import IOP
from Hero.cra import CRA
from Hero.zobal import ZOBAL
from Hero.eniripsa import ENIRIPSA
from Hero.xelor import XELOR
from Hero.sacrieur import SACRIEUR
from Hero.enutrof import ENUTROF
from Hero.feca import FECA
from Hero.steamer import STEAMER
from Hero.pandawa import PANDAWA
from Hero.Ennemy import Ennemy
import random
import re
import logging
from core.utils import isControlledByAI
logger = logging.getLogger(__name__)
iop = IOP()
cra = CRA()
eniripsa = ENIRIPSA()
xelor = XELOR()
enutrof = ENUTROF()
sacrieur = SACRIEUR()
zobal = ZOBAL()
steamer = STEAMER()
pandawa = PANDAWA()
feca = FECA()
actualFight = None
GameHeroes = [iop, cra, eniripsa, xelor, enutrof, sacrieur, zobal, feca, steamer, pandawa]
EnnemyList = []

def handleNewFight():
    from core.calc import PlayedHeroes
    from core.extractData import extractData
    from core.interface_support import resetListbox
    if PlayedHeroes:
        extractData(PlayedHeroes)
        for hero in PlayedHeroes :
            hero.clear()
        PlayedHeroes.clear()
    if EnnemyList:
        EnnemyList.clear()
    PlayedHeroes = []
    resetListbox()
    global actualFight
    actualFight = random.randint(1000, 99999)

def NewHero(line) :
    from core.calc import PlayedHeroes
    matchNumber = re.search(r"breed\s*:\s*(\d+)", line)
    fighter_name = re.search(r'fightId=[0-9]* (.*?) breed : ', line)
    AI = isControlledByAI(line)
    for hero in PlayedHeroes :
        logger.debug(f"Debug : {hero.name} =?!= {fighter_name}")
        if hero.name == fighter_name.group(1) :
            return
    if matchNumber :
        classNumber = int(matchNumber.group(1))
        fighter_name = fighter_name.group(1)
        if classNumber > 0 and classNumber <= 18 and AI == False:
            for hero in GameHeroes :
                if hero.breed == classNumber :
                    hero.name = fighter_name
                    PlayedHeroes.append(hero)
        else :
            EnnemyList.append(Ennemy(fighter_name, classNumber))
            #TO DO
