from core.utils import TotalAmountOfDamage, TotalAmountOfHeal, extractPlayerName, update_hero_rankings, checkIndirectCompatibility
from core.interface_support import updateHeroValue
from Hero.GameHeroes import GameHeroes
import re
from Hero.spell import Spell
import logging

logger = logging.getLogger(__name__)

PlayedHeroes = []

lastHeroes = None
lastIndirectHeroes = None

def parseSpellInLine(line):
    global lastHeroes, lasIndirectHeroes
    pattern = re.compile(
        r"\b(?P<name>[A-ZÉÈÊÂÎÔÛÄËÏÖÜÀÇ][\w\-]*(?:\s+[A-ZÉÈÊÂÎÔÛÄËÏÖÜÀÇ]?[a-zéèêëàùûüîïôöç'\-]+)*)\s+"
        r"(?P<action>lance le sort|utilise l'objet)\s+"
        r"(?P<spell>[^(]+?)(?:\s*\([^)]*\))?$"
    )
    match = pattern.search(line)
    if match :
        CurrentName = match.group("name").strip()
        #action = match.group("action")
        spellMatch = match.group("spell")
        #logger.debug(f"debug new parsespell with CAC {CurrentName} - {action} - {spellMatch}")
        for hero in PlayedHeroes:
            for Invo in hero.InvocList :
                logger.debug(f"nom de l'invoc {Invo.name}")
            logger.debug(f"currentName {CurrentName}")
            if CurrentName == hero.name or hero.InvocList and any(CurrentName == invo.name for invo in hero.InvocList):
                lastHeroes = hero
                spell = hero.getSpell(spellMatch)
                if spell :
                    logger.debug(f"used spell {spell.name} by {hero.name}")
                    hero.UsedSpell.append(spell)
                    return spell
                return None
    lastHeroes = None
    lastIndirectHeroes = None
    return None

def parseDamageInLine(line):
    global lastHeroes, lastIndirectHeroes
    parsedIndirect = None
    match = re.search(r"([+-])\s*([\d\s ]+)\s*PV", line)
    element = re.search(r'PV\s*\(([^)]+)\)', line)
    indirect = re.search(r'\(([^()]*)\)(?!.*\([^()]*\))', line)
    Target = re.search(r"\[Information \(combat\)\]\s+([^:]+):\s*-[\d\s ]+PV", line)

    if Target and lastHeroes and lastHeroes.name == Target.group(1).strip() :
        return
    if match:
        sign = match.group(1)   
        value = re.sub(r'\D', '', match.group(2))  # nettoyage espaces
        if element :
            parsedElement = element.group(1)
        if indirect :
            parsedIndirect = indirect.group(1)
            indirectHero = checkIndirectCompatibility(parsedIndirect, PlayedHeroes)
            print(f"Debug : {indirectHero}")
            if indirectHero :
                lastIndirectHeroes = indirectHero
            else :
                parsedIndirect = None
                lastIndirectHeroes = None
            logger.debug(f"indirect -->  {parsedIndirect}")
        return {"sign": sign, "value": value, "element": parsedElement, "indirect": parsedIndirect} 
    return None

def parseShieldInLine(line):
    global lastHeroes, lastIndirectHeroes
    pattern = r'(\d[\d\u00A0\u202F ]*)(?=\s*Armure\b)'
    match = re.search(pattern, line, flags=re.IGNORECASE)
    indirect = re.search(r'\(([^()]*)\)(?!.*\([^()]*\))', line)
    if not match:
        return None

    raw_number = match.group(1)
    cleaned = re.sub(r'[\s\u00A0\u202F]', '', raw_number)
    if indirect :
        parsedIndirect = indirect.group(1)
        indirectHero = checkIndirectCompatibility(parsedIndirect, PlayedHeroes)
        print(f"Debug WTF PK CA RENVOIE UN SORT : {indirectHero}")
        if indirectHero :
            lastIndirectHeroes = indirectHero
        else :
            parsedIndirect = None
            lastIndirectHeroes = None
        logger.debug(f"indirect --> {parsedIndirect}")
    try:
        value = int(cleaned)
    except ValueError:
        return None

    logger.debug(f"nombre d'armure trouve : {value}")
    return {"sign": "+", "value": value, "element": "Shield", "indirect": parsedIndirect}
    
def handle_spell(line):
    global lastHeroes, lastIndirectHeroes

    IncomingValue = parseDamageInLine(line)
    logger.debug(f"Debug last hero handle Spell : {lastHeroes} {lastIndirectHeroes}")

    if not IncomingValue:
        return

    target_hero = None
    if IncomingValue["indirect"] and lastIndirectHeroes:
        target_hero = lastIndirectHeroes
    elif IncomingValue["indirect"] is None and lastHeroes:
        target_hero = lastHeroes

    if not target_hero:
        return

    # Recherche du héros correspondant dans PlayedHeroes
    value = int(IncomingValue["value"])
    sign = IncomingValue["sign"]
    element = IncomingValue["element"]
    logger.debug(f"debug depuis HANDLE SPELL {IncomingValue["indirect"]} - {element}")
    for hero in PlayedHeroes:
        if hero.name == target_hero.name:
            if sign == '+':
                hero.HealDone.append(value)
                hero.TotalAmountOfHeal += value
            else:
                hero.DamageDone.append(value)
                hero.TotalAmountOfDamage += value
            break
    update_hero_rankings(PlayedHeroes)
    updateHeroValue(PlayedHeroes)

def handleShield(line) :
    global lastHeroes, lastIndirectHeroes
    IncomingValue = parseShieldInLine(line)

    logger.debug(f"Debug last hero handle Spell : {lastHeroes} {lastIndirectHeroes}")

    if not IncomingValue:
        return 
    
    target_hero = None 
    if IncomingValue["indirect"] and lastIndirectHeroes:
        target_hero = lastIndirectHeroes
    elif IncomingValue["indirect"] is None and lastHeroes:
        target_hero = lastHeroes

    if not target_hero :
        return
    value = int(IncomingValue["value"])
    sign = IncomingValue["sign"]
    element = IncomingValue["element"]
    logger.debug(f"debug depuis HANDLE SHIELD {IncomingValue["indirect"]} - {element}")
    for hero in PlayedHeroes:
        if hero.name == target_hero.name:
            hero.ShieldDone.append(value)
            hero.TotalAmountOfShield += value
            break
    update_hero_rankings(PlayedHeroes)
    updateHeroValue(PlayedHeroes)

def ResetCalc():
    lastHeroes = None
    lastIndirectHeroes = None