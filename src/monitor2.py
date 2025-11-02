from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import os
import platform
import time
import re 
from core.calc import handle_spell, parseSpellInLine, handleShield, ResetCalc, EndOfTurn
from Hero.GameHeroes import handleNewFight, NewHero, GenerateRapport, handleInvoc
import logging
import sys
import tkinter.filedialog as filedialog

# Configuration simple
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class MyHandler(FileSystemEventHandler):
    MultiMode = False
    MultiModeList = []
    CreationCount = 0
    countcase = 0
    def __init__(self, file_path):
        self.file = Path(file_path)
        self.position = 0
        logging.info(f"Initialisation du handler pour {self.file}")

        # Lecture initiale (ignore le contenu existant)
        if self.file.exists():
            with open(self.file, "r", encoding="utf-8") as f:
                f.seek(0, 2)
                self.position = f.tell()

    def MultiModeTrim(self, line):
        result = re.sub(r"(?<=\bINFO)\s*\d{2}:\d{2}:\d{2},\d{3}\s*", " ", line, flags=re.IGNORECASE)
        result = re.sub(r"\s{2,}", " ", result)

        if result in self.MultiModeList:
            self.MultiModeList.remove(result)
            return 1
        else:
            self.MultiModeList.append(result)
            self.countcase += 1
            if self.countcase == 10000 :
                self.countcase = 0
                self.MultiModeList.clear()
            return 0
    def process_file(self):
        if not self.file.exists():
            return

        with open(self.file, "r", encoding="utf-8", errors='ignore') as f:
            f.seek(self.position)
            new_content = f.read()

            if not new_content:
                return  # Rien de nouveau attention potentiel sortie de programme 

            allNewLine = new_content.split("\n")
            for l in allNewLine:
                if not l.strip():
                    continue
                if l.startswith(" INFO "):
                    logging.debug(f"Debug start with INFO: {l}")
                    if "CREATION DU COMBAT" in l:
                        self.CreationCount +=1
                        if self.CreationCount == 2 :
                            self.MultiMode = True
                            continue
                        handleNewFight()
                        logging.info("Nouveau combat détecté")
                    elif self.MultiMode and self.MultiModeTrim(l) == 1:
                        #logging.debug(f"Debug : MultiMode Line trimmed {l}")
                        continue
                    elif "eRL:1407" in l:
                        NewHero(l)
                    elif "[Information (combat)]" in l:
                        if "lance le sort" in l or "utilise l'objet" in l:
                            parseSpellInLine(l)
                        elif "PV" in l:
                            handle_spell(l)
                        elif "Armure" in l:
                            handleShield(l)
                        elif "Invoque un" in l:
                            handleInvoc(l)
                        elif "secondes reportées pour le tour suivant." in l:
                            EndOfTurn(l)
                    elif self.CreationCount > 0 and "aVi:92" in l or "Combat terminé, cliquez ici pour rouvrir l'écran de fin de combat." in l: #rajouter fin de combat classique
                        self.MultiModeList.clear()
                        self.MultiMode = False
                        self.CreationCount = 0
                        self.countcase = 0
                        logging.debug(f"fin du combat {self.MultiMode} - {self.CreationCount}")
                        GenerateRapport()
                        ResetCalc()
            self.position = f.tell()

    def on_modified(self, event):
        if Path(event.src_path).name == self.file.name:
            self.process_file()

    def on_created(self, event):
        if Path(event.src_path).name == self.file.name:
            logging.info(f"{self.file.name} recréé, réinitialisation du suivi")
            self.position = 0 
            self.process_file()

    def on_moved(self, event):
        if Path(event.src_path).name == self.file.name:
            logging.info(f"{self.file.name} déplacé vers {event.dest_path}")
            self.position = 0 

    def on_deleted(self, event):
        if Path(event.src_path).name == self.file.name:
            logging.info(f"{self.file.name} supprimé")
            self.position = 0

def getWakfuLogsPath() :
    system = platform.system().lower()
    print(system)
    if system == "windows" : 
        base = Path(os.getenv("APPDATA", Path.home() / "AppData/Roming"))
        print(f"{base}")

    # MACOS TO DO
    elif system == "darwin":  # macOS
        base = Path.home() / "Library/Application Support"
    
    #LINUX/AUTRE TO DO
    else:  # Linux / autres Unix
        # Exemple : ~/.config/zaap/gamesLogs/wakfu/logs/wakfu.log
        base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))

    return base / "zaap" / "gamesLogs" / "wakfu" / "logs" / "wakfu.log"

file = getWakfuLogsPath()
print(f"{file}")
fileCheck = Path(file)
if not fileCheck.exists():
    file = filedialog.askopenfilename(
        title="Trouvez votre fichier wakfu.log",
    )
    print(f"fichier choisis {file}  or {Path(file)}")
    logging.info(f"fichier choisis par l'utilisateur : {file}")
    fileCheck = Path(file)
    if not file :
        sys.exit()
from core import interface_support
event_handler = MyHandler(file)
observer = PollingObserver()
observer.schedule(event_handler, str(fileCheck.parent), recursive=False)
observer.start()
interface_support.main()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()