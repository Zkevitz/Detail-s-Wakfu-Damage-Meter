from core.utils import TotalAmountOfDamage, TotalAmountOfHeal, extractPlayerName, update_hero_rankings, checkIndirectCompatibility
from core.interface_support import updateHeroValue
from Hero.GameHeroes import GameHeroes
import re
from Hero.spell import Spell
import logging

logger = logging.getLogger(__name__)

PlayedHeroes = []
lastHeroes = None
def parseSpellInLine(line):
    global lastHeroes
    match = re.search(r"lance le sort\s+([^(]+?)(?:\s*\([^)]*\))?$", line)
    NameSearch = re.search(r"\b([A-ZÉÈÊÂÎÔÛÄËÏÖÜÀÇ][\w\-]*(?:\s+[A-ZÉÈÊÂÎÔÛÄËÏÖÜÀÇ]?[a-zéèêëàùûüîïôöç'\-]+)*)\s+lance le sort\b", line)
    if match :
        CurrentName = NameSearch.group(1).strip()
        match = match.group(1).strip()
        for hero in PlayedHeroes:
            if CurrentName == hero.name:
                lastHeroes = hero
                spell = hero.getSpell(match)
                if spell :
                    logger.debug(f"used spell {spell.name} by {hero.name}")
                    hero.UsedSpell.append(spell)
                    return spell
                return None
    lastHeroes = None
    return None

def parseDamageInLine(line):
    global lastHeroes
    match = re.search(r"([+-])\s*([\d\s ]+)\s*PV", line)
    element = re.search(r'PV\s*\(([^)]+)\)', line)
    indirect = re.search(r'\(([^()]*)\)(?!.*\([^()]*\))', line)
    if match:
        sign = match.group(1)   
        value = re.sub(r'\D', '', match.group(2))  # nettoyage espaces
        if element :
            parsedElement = element.group(1)
        if indirect :
            parsedIndirect = indirect.group(1)
            indirectHero = checkIndirectCompatibility(parsedIndirect, PlayedHeroes)
            if indirectHero :
                lastHeroes = indirectHero
                logger.debug("indirect --> ", parsedIndirect)
        return {"sign": sign, "value": value, "element": parsedElement, "indirect": parsedIndirect} 
    return None

def parseShieldInLine(line):
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
        if indirectHero :
            lastHeroes = indirectHero
        logger.debug(f"indirect --> {parsedIndirect}")
    try:
        value = int(cleaned)
    except ValueError:
        return None

    logger.debug(f"nombre d'armure trouve : {value}")
    return {"sign": "+", "value": value, "element": "Shield", "indirect": parsedIndirect}
    
def handle_spell(line):
    global lastHeroes
    IncomingValue = parseDamageInLine(line)
    logger.debug(f"Debug last hero handle Spell : {lastHeroes}")
    if IncomingValue and lastHeroes:
        for hero in PlayedHeroes:
            if lastHeroes != None and hero.name == lastHeroes.name:
                if IncomingValue["sign"] == '+' and IncomingValue["element"] != "Shield":
                    hero.HealDone.append(int(IncomingValue["value"]))
                    hero.TotalAmountOfHeal += int(IncomingValue["value"])
                elif IncomingValue["element"] == "Shield":
                    hero.ShieldDone.append(int(IncomingValue["value"]))
                    hero.TotalAmountOfShield += int(IncomingValue["value"])
                else :
                    hero.DamageDone.append(int(IncomingValue["value"]))
                    hero.TotalAmountOfDamage += int(IncomingValue["value"])
                break      
        update_hero_rankings(PlayedHeroes)
        updateHeroValue(PlayedHeroes)

def handleShield(line) :
    IncomingValue = parseShieldInLine(line)
    if IncomingValue :
        for hero in PlayedHeroes: 
            if lastHeroes != None and hero.name == lastHeroes.name :
                hero.ShieldDone.append(int(IncomingValue["value"]))
                hero.TotalAmountOfShield += int(IncomingValue["value"])
                break
        update_hero_rankings(PlayedHeroes)
        updateHeroValue(PlayedHeroes)