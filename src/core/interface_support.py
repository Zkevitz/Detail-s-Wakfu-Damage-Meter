import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import customtkinter as ctk
import tkinter.messagebox as msgbox 
import tkinter.filedialog as filedialog
import core.interface
from core.utils import formatNumber
from core.extractData import extractData, loadHeroesFromJson, getEnnemyEntitieFromJson
from functools import partial
from collections import Counter
from core.image import trashIcon
import os
import logging

logger = logging.getLogger(__name__)
DisplayMode = "Damage"
#_debug = True 

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
    if DisplayMode == "Damage" :
        for hero in PlayedHeroes:
            _w1.Listbox1.delete(hero.DamageRank - 1)
            _w1.Listbox1.insert(hero.DamageRank - 1 , f"{hero.DamageRank} - {hero.name} [{hero.className}] : {formatNumber(hero.TotalAmountOfDamage)}")
            _w1.Listbox1.itemconfig(hero.DamageRank - 1, fg="black", bg=hero.color)
    elif DisplayMode == "Heal" :
        for hero in PlayedHeroes:
            _w1.Listbox1.delete(hero.HealRank - 1)
            _w1.Listbox1.insert(hero.HealRank - 1 , f"{hero.HealRank} - {hero.name} [{hero.className}] : {formatNumber(hero.TotalAmountOfHeal)}") 
            _w1.Listbox1.itemconfig(hero.HealRank - 1, fg="black", bg=hero.color)
    elif DisplayMode == "Shield" :
        for hero in PlayedHeroes:
            _w1.Listbox1.delete(hero.ShieldRank - 1)
            _w1.Listbox1.insert(hero.ShieldRank - 1 , f"{hero.ShieldRank} - {hero.name} [{hero.className}] : {formatNumber(hero.TotalAmountOfShield)}") 
            _w1.Listbox1.itemconfig(hero.ShieldRank - 1, fg="black", bg=hero.color)

def displayDataOnListFirstTime(PlayedHeroes):
    resetListbox()
    if DisplayMode == "Damage" :
        sorted_heroes = sorted(PlayedHeroes, key=lambda h: h.DamageRank)
        for hero in sorted_heroes:
            _w1.Listbox1.insert("end", f"{hero.DamageRank} - {hero.name} [{hero.className}] : {formatNumber(hero.TotalAmountOfDamage)}")
            _w1.Listbox1.itemconfig("end", fg="black", bg=hero.color)
    elif DisplayMode == "Heal" :
        sorted_heroes = sorted(PlayedHeroes, key=lambda h: h.HealRank)
        for hero in sorted_heroes:
            _w1.Listbox1.insert("end", f"{hero.HealRank} - {hero.name} [{hero.className}] : {formatNumber(hero.TotalAmountOfHeal)}")
            _w1.Listbox1.itemconfig("end", fg="black", bg=hero.color)
    elif DisplayMode == "Shield" :
        sorted_heroes = sorted(PlayedHeroes, key=lambda h: h.ShieldRank)
        for hero in sorted_heroes:
            _w1.Listbox1.insert("end", f"{hero.ShieldRank} - {hero.name} [{hero.className}] : {formatNumber(hero.TotalAmountOfShield)}")
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

def enforce_topmost(root):
    root.attributes('-topmost', True)
    root.lift()

def on_focus_out(event):
    enforce_topmost(event.widget)

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
    if choice == "Reset" :
        resetButton()
    elif choice == "History" :
        ShowHistory()
    elif choice == "Import Data" :
        importdata()
    _w1.Parametres.configure(variable=ctk.StringVar(value="Options"))

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

        
    def toggleHistory(frameDetails, ToggleBtn):
        if frameDetails.winfo_viewable():
            frameDetails.grid_remove()
            ToggleBtn.configure(text="▸")
        else :
            frameDetails.grid()
            ToggleBtn.configure(text="▾")

    scrolableFrame = ctk.CTkScrollableFrame(window, label_text="Rapport History")
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
                width=40,
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
            #ctk.CTkLabel(frameDetails, text=f"Détails de {nom_fichier}").pack(anchor="w", pady=2)
            #ctk.CTkLabel(frameDetails, text=f"Chemin : {chemin_complet}").pack(anchor="w", pady=2)
            #ctk.CTkLabel(frameDetails, text=f"Taille : {os.path.getsize(chemin_complet)} octets").pack(anchor="w", pady=2)
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

    root.attributes('-topmost', True)
    root.lift()
    global _top1, _w1
    _top1 = root
    _w1 = interface.Toplevel1(_top1)
    interface._w1 = _w1

    root.mainloop()

if __name__ == '__main__':
    main()


#PASSER LA RECONAISANCE DE PERSO GRACE AU NOM ET LAISSE LA COMPARAISON AU SORT UNIQUEMENT POUR L'INDIRECT 
