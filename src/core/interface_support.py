import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import customtkinter as ctk
import tkinter.messagebox as msgbox 
import tkinter.filedialog as filedialog
import core.interface
from core.utils import formatNumber
from core.extractData import extractData, loadHeroesFromJson
from functools import partial
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
    window.attributes('-topmost', True)
    window.attributes("-alpha", 0.8)
    window.lift()

    scrolableFrame = ctk.CTkScrollableFrame(window, label_text="Rapport History")
    scrolableFrame.pack(fill="both", expand=True, padx=10, pady=10)
    for i, nom_fichier in enumerate(os.listdir("Rapport")):
        chemin_complet = os.path.join("Rapport", nom_fichier)
        if os.path.isfile(chemin_complet):
            label = ctk.CTkLabel(scrolableFrame, text=nom_fichier)
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            bouton = ctk.CTkButton(
                scrolableFrame,
                text="Ouvrir",
                width=40,
                height=10,
                command=lambda p=chemin_complet: [loadHeroesFromJson(p, PlayedHeroes), displayDataOnListFirstTime(PlayedHeroes)]
            )
            bouton.grid(row=i, column=1, padx=10, pady=5, sticky="e")
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
