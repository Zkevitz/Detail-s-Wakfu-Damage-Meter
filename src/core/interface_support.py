import sys
from tkinter.constants import *
import customtkinter as ctk
import tkinter.messagebox as msgbox 
import tkinter.filedialog as filedialog
from core.utils import formatNumber
from core.extractData import extractData, loadHeroesFromJson, getEnnemyEntitieFromJson
from functools import partial
from collections import Counter
from core.image import trashIcon
import os
import logging

logger = logging.getLogger(__name__)
DisplayMode = "Damage"

mode_map = {
    "Damage": ("DamageRank", "TotalAmountOfDamage"),
    "Heal": ("HealRank", "TotalAmountOfHeal"),
    "Shield": ("ShieldRank", "TotalAmountOfShield"),
}

def resetButton():
    if _w1 is None:
        msgbox.showerror("Erreur", "L’interface n’est pas encore initialisée.")
        return
    reponse = msgbox.askokcancel("Reset", "ceci entrainera la perte de données du combat actuel voulez vous continuer ?")
    if reponse:
        from core.calc import PlayedHeroes
        for hero in PlayedHeroes:
            hero.clear()
        PlayedHeroes.clear()
        resetListbox()
        msgbox.showinfo("Réinitialisation", "Réinitialisation effectuée")

def resetListbox(): 
    _w1.Listbox1.delete(0, 'end')


def updateHeroValue(PlayedHeroes):
    if _w1 is None:
        msgbox.showerror("Erreur", "L’interface n’est pas encore initialisée.")
        return
    displayDataOnList(PlayedHeroes)

def displayDataOnList(PlayedHeroes):
    if _w1.Listbox1.size() == 0 :
        displayDataOnListFirstTime(PlayedHeroes)
        return

    if DisplayMode not in mode_map:
        logger.warning(f"DisplayMode inconnu : {DisplayMode}")
        return
    
    rank_attr, total_attr = mode_map[DisplayMode]

    for hero in PlayedHeroes:
        rank = getattr(hero, rank_attr)
        total = getattr(hero, total_attr)
        perturn = total / hero.PlayedTurn if hero.ini > 0 else "(??)"

        text = f"{rank} - {hero.name} [{hero.className}] : {formatNumber(total)} / {formatNumber(perturn) if perturn != '(??)' else perturn}"
        _w1.Listbox1.delete(rank - 1)
        _w1.Listbox1.insert(rank - 1, text)
        _w1.Listbox1.itemconfig(rank - 1, fg="black", bg=hero.color)
        logger.debug(f"{hero.name} ({DisplayMode}) : total={total}, tours={hero.PlayedTurn}, rank={rank}")


def displayDataOnListFirstTime(PlayedHeroes):
    resetListbox()
    if DisplayMode not in mode_map:
        logger.warning(f"DisplayMode inconnu : {DisplayMode}")
        return

    rank_attr, total_attr = mode_map[DisplayMode]
    sorted_heroes = sorted(PlayedHeroes, key=lambda h: getattr(h, rank_attr))

    for hero in sorted_heroes:
        total = getattr(hero, total_attr)
        rank = getattr(hero, rank_attr)
        perturn = total / hero.PlayedTurn if hero.ini > 0 else "(??)"
        text = f"{rank} - {hero.name} [{hero.className}] : {formatNumber(total)} / {formatNumber(perturn) if perturn != '(??)' else perturn}"
        _w1.Listbox1.insert("end", text)
        _w1.Listbox1.itemconfig("end", fg="black", bg=hero.color)

def switchButton(mode):
    logger.debug(f"mode = {mode}")
    if _w1 is None:
        msgbox.showerror("Erreur", "L’interface n’est pas encore initialisée.")
        return
    _w1.Listbox1.delete(0, 'end')
    logger.info(f"{mode} button clicked")
    global DisplayMode
    DisplayMode = mode
    from core.calc import PlayedHeroes
    displayDataOnListFirstTime(PlayedHeroes)

def extractdata():
    from core.calc import PlayedHeroes
    outputFileName = extractData(PlayedHeroes)
    msgbox.showinfo("Export terminé", f"Export terminé : {outputFileName} ({len(PlayedHeroes)} héros exportés)")


def importdata():
    from core.calc import PlayedHeroes
    file = None
    reponse = msgbox.askyesno(
        title="Confirmation",
        message="L'importation de données va effacer les données actuelles. Voulez-vous vraiment effectuer cette action ?"
    )
    if reponse:
        from calc import PlayedHeroes
        for hero in PlayedHeroes:
            hero.clear()
        PlayedHeroes.clear()
        resetListbox()
        file = chooseFileForImport()
    if file == None :
        return
    PlayedHeroes = loadHeroesFromJson(file, PlayedHeroes)
    displayDataOnListFirstTime(PlayedHeroes)

def chooseFileForImport():
    file = filedialog.askopenfilename(
        title="Choisissez un fichier JSON",
        filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
    )
    if file:
        msgbox.showinfo("Fichier sélectionné", f"Vous avez choisi :\n{file}")
        logger.debug("Fichier choisi :", file)
        return file
    else:
        msgbox.showwarning("Aucun fichier", "Aucun fichier n’a été sélectionné.")
        return None
    
def open_settings(choice):
    logger.debug(f"{choice} MENU button clicked")
    if choice == "🔁" : #old option
        resetButton()
    elif choice == "📋" :
        ShowHistory()
    elif choice ==  "✕" :
        onWindowClose() 
    elif choice == "🔒": 
        _w1.lockButton.configure(text="🔓", command=lambda i="🔓" : open_settings(i))
        _w1.lock = False
        _w1.resize_grip.place(relx=0.0, rely=1.0, anchor="sw")
    elif choice == "🔓" :
        _w1.lockButton.configure(text="🔒", command=lambda i="🔒" : open_settings(i))
        _w1.lock = True
        _w1.resize_grip.place_forget()
    elif choice == "Import Data" : #old option
        importdata()

def ShowHistory():
    from core.calc import PlayedHeroes
    window = ctk.CTkToplevel(root)
    window.title("History")
    window.geometry("360x300")
    window.attributes('-topmost', True)
    window.attributes("-alpha", 0.8)
    window.lift()

    rows = {}
    
    def DeleteRapport(index, chemin_complet) :
        if os.path.exists(chemin_complet):
            os.remove(chemin_complet)
            logger.debug(f"supression du fichier --> : {chemin_complet}")
        
        for widget in rows[index].values():
            if hasattr(widget, "destroy"):
                widget.destroy()

    def DeleteAllRapport():
        print("bouton appuyer")
        for i, data in list(rows.items()):
            DeleteRapport(i, data["path"])
            
        
    def toggleHistory(frameDetails, ToggleBtn):
        if frameDetails.winfo_viewable():
            frameDetails.grid_remove()
            ToggleBtn.configure(text="▸")
        else :
            frameDetails.grid()
            ToggleBtn.configure(text="▾")


    # Parentheader = ctk.CTkFrame(window)
    # Parentheader.pack(fill="both", expand=True, padx=10, pady=10)

    header = ctk.CTkFrame(window, fg_color="transparent")
    header.pack(fill="x")

    title = ctk.CTkLabel(header, text="Rapport History", font=("Arial", 16, "bold"))
    title.pack(side="top", padx=(0, 10))

    DeleteAllButton = ctk.CTkButton(header, text="Delete All", command=DeleteAllRapport)
    DeleteAllButton.pack(side="top")
    scrolableFrame = ctk.CTkScrollableFrame(header)
    scrolableFrame.pack(fill="both", expand=True, padx=10, pady=10)


    fichiers = sorted(
        [f for f in os.listdir("Rapport") if os.path.isfile(os.path.join("Rapport", f))],
        key=lambda f: os.path.getmtime(os.path.join("Rapport", f)),
        reverse=True
    )
    for i, nom_fichier in enumerate(fichiers):
        chemin_complet = os.path.join("Rapport", nom_fichier)
        if os.path.isfile(chemin_complet):
            Ennemies = getEnnemyEntitieFromJson(chemin_complet)

            ToggleButton = ctk.CTkButton(scrolableFrame, text="▸", width=10, height=10, fg_color="transparent", hover_color="#2615c0", command=None)
            ToggleButton.grid(row=i*2, column=0, padx=(5, 0))
            nom_fichier = nom_fichier[:-5]
            if len(nom_fichier) >= 27 :
                nom_fichier = nom_fichier[:27]
            label = ctk.CTkLabel(scrolableFrame, text=nom_fichier)
            label.grid(row=i*2, column=2, sticky="w", padx=5, pady=0)
            DeleteButton = ctk.CTkButton(scrolableFrame, image=trashIcon, text="", width=10, height=10, fg_color="transparent", hover_color="#ff6666", command=lambda idx=i , f=chemin_complet : DeleteRapport(idx, f))
            DeleteButton.grid(row=i*2, column=1, sticky="w", padx=0, pady=0)
            bouton = ctk.CTkButton(
                scrolableFrame,
                text="Ouvrir",
                width=30,
                height=10,
                command=lambda p=chemin_complet: [loadHeroesFromJson(p, PlayedHeroes), displayDataOnListFirstTime(PlayedHeroes)]
            )
            bouton.grid(row=i*2, column=3, padx=0, pady=0, sticky="w")

            frameDetails = ctk.CTkFrame(scrolableFrame)
            frameDetails.grid(row=i*2+1, column=1, columnspan=2, sticky="w", padx=40, pady=(0, 10))
            frameDetails.grid_remove()
            counts = Counter(e["name"] for e in Ennemies)
            for name, count in counts.items():
                ctk.CTkLabel(frameDetails, text=f"{name} x {count}").pack(anchor="w", pady=1)
            ToggleButton.configure(command=lambda f=frameDetails, b=ToggleButton: toggleHistory(f, b))

            rows[i] = {
                "path": chemin_complet,
                "toggle": ToggleButton,
                "label": label,
                "delete": DeleteButton,
                "open": bouton,
                "details": frameDetails
            }


        

def onWindowClose():
    root.destroy()
    sys.exit()

from core import interface
def main(*args):
    global root
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.protocol('WM_DELETE_WINDOW', onWindowClose)
    root.attributes("-alpha", 0.8)

    # POUR RETRAVAILLER LE HEADER
    root.overrideredirect(True)

    root.attributes('-topmost', True)
    root.lift()
    global _top1, _w1
    _top1 = root
    _w1 = interface.Toplevel1(_top1)
    interface._w1 = _w1

    root.mainloop()

if __name__ == '__main__':
    main()
