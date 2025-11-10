import sys
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter.constants import *
from tkinter import font
import os.path
from PIL import Image, ImageTk
from functools import partial
_location = os.path.dirname(__file__)
from core import interface_support
_headerbgcolor = '#111724'
_fgcolor = 'black'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
        top is the toplevel containing window.'''
        self.lock = True
        self.resizing = False
        self.min_width = 290
        self.min_height = 190 
        self.largeur = 300
        self.hauteur = 200
        self._is_maximized = False
        self.title = "Detail's Wakfu"
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        self.x = screen_width - self.largeur - 10
        self.y = 10
        top.geometry(f"{self.largeur}x{self.hauteur}+{self.x}+{self.y}")
        top.title(self.title)

        self.top = top

        self.optionmenu_var = ctk.StringVar(value="Damage")

        self.CreateSegButton()
        self.CreateListBox()
        self.CreateHeader()
        self.CreateResizeGrip()

        self.header_frame.bind("<Button-1>", self.startMove)
        self.header_frame.bind("<B1-Motion>", self.MoveWindow)
        # self.status_label.bind("<Button-1>", self.startMove)
        # self.status_label.bind("<B1-Motion>", self.MoveWindow)
        self.title_label.bind("<Button-1>", self.startMove)
        self.title_label.bind("<B1-Motion>", self.MoveWindow)

    def CreateResizeGrip(self):
        self.resize_grip = ctk.CTkFrame(self.top, width=10, height=10, fg_color="#a3a3a3")
        self.resize_grip.place(relx=0.0, rely=1.0, anchor="sw")

        self.emoji_label = ctk.CTkLabel(self.resize_grip, text="↙️", text_color="white", font=("Arial", 12))
        self.emoji_label.place(relx=0.5, rely=0.5, anchor="center")
        # Changer le curseur (si supporté)
        self.resize_grip.configure(cursor="size_ne_sw")

        # Bind les événements souris

        self.emoji_label.bind("<Button-1>", self.startResize)
        self.emoji_label.bind("<B1-Motion>", self.doResize)
        self.emoji_label.bind("<ButtonRelease-1>", self.stopResize)
        self.resize_grip.bind("<Button-1>", self.startResize)
        self.resize_grip.bind("<B1-Motion>", self.doResize)
        self.resize_grip.bind("<ButtonRelease-1>", self.stopResize)

        if self.lock :
            self.resize_grip.place_forget()

    def startResize(self, event):
        if self.lock :
            return 
        self.resizing = True
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.start_width = self.top.winfo_width()
        self.start_height = self.top.winfo_height()
        self.start_pos_x = self.top.winfo_x()
        self.start_pos_y = self.top.winfo_y()

    def stopResize(self, event):
        self.resizing = False

    def doResize(self, event):
        if not self.resizing:
            return
        
        if self.lock : 
            return
    
        dx = event.x_root - self.start_x
        dy = event.y_root - self.start_y

        # Agrandissement horizontal vers la gauche
        new_width = max(self.min_width, self.start_width - dx)
        new_height = max(self.min_height, self.start_height + dy)

        if new_width <= self.min_width or new_height <= self.min_height :
            return 

        # On déplace la fenêtre pour garder le coin droit fixe
        new_x = self.start_pos_x + dx

        self.top.geometry(f"{int(new_width)}x{int(new_height)}+{int(new_x)}+{int(self.start_pos_y)}")

    def startMove(self, event):
        if self.lock == True :
            return
        self._x = event.x
        self._y = event.y
    
    def MoveWindow(self, event):
        if self.lock == True : 
            return 
        if self._is_maximized == True :
            return
        self.x = self.top.winfo_pointerx() - self._x
        self.y = self.top.winfo_pointery() - self._y
        self.top.geometry(f"+{self.x}+{self.y}")
        
    def CreateSegButton(self):
        self.segButton = ctk.CTkSegmentedButton(
            self.top, 
            values=["Damage", "Heal", "Shield"],
            variable=self.optionmenu_var, 
            command=interface_support.switchButton,
            corner_radius=0 
        )
        self.segButton.set("Damage")
        self.segButton.place(relx=0.00, rely=0.15, relwidth=1.00)
        self.segButton.configure(fg_color="grey")

    def CreateListBox(self):
        self.Listbox1 = tk.Listbox(self.top)
        self.Listbox1.place(relx=0.0, rely=0.30, relheight=0.76
                , relwidth=1.008)
        self.Listbox1.configure(background="grey")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(exportselection="0")
        grande_police = font.Font(family="Segoe UI", size=12, weight="bold")
        self.Listbox1.configure(font=grande_police)
        self.Listbox1.configure(foreground="black")
        self.Listbox1.configure(highlightbackground="#000001")
        self.Listbox1.configure(highlightcolor="black")
        self.Listbox1.configure(selectbackground="#d9d9d9")
        self.Listbox1.configure(selectforeground="black")
        self.Listbox1.configure(bd=0)
        self.Listbox1.configure(relief="flat")
        self.Listbox1.configure(highlightthickness=0)

    def ShowSettingsMenu(self, event=None):
        menu = tk.Menu(self.top, tearoff=0, bg="#333", fg="white", activebackground="#555", activeforeground="white")
        menu.add_command(label="Reset", command=lambda i = "🔁": interface_support.open_settings(i))
        menu.add_separator()
        menu.tk_popup(event.x_root, event.y_root)

    def CreateHeader(self):
        self.header_frame = ctk.CTkFrame(self.top, fg_color=_headerbgcolor, height=30)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame._corner_radius = 0
        self.header_frame.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Detail's Wakfu",
            font=("Arial", 14, "bold"),
            text_color="#4a9eff"
        )
        self.title_label.pack(side="left", padx=5, pady=5)

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="En attente...",
            font=("Arial", 10),
            text_color="#888"
        )
        self.status_label.pack(side="left", padx=5)

        self.buttons_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.buttons_frame.pack(side="left", padx=2)

        for icon in ["📋", "⚙️", "🔒", "✕"]:
            optionmenu_var = ctk.StringVar(value=icon)
            btn = ctk.CTkButton(
                self.buttons_frame,
                text=icon,
                width=12,
                height=12,
                fg_color="transparent",
                hover_color="#000001",
                font=("Arial", 12)
            )
            if icon == "⚙️" :
                btn.bind("<Button-1>", self.ShowSettingsMenu)
            else :
                btn.configure(command=lambda i=icon: interface_support.open_settings(i))
            if icon == "🔒" : 
                self.lockButton = btn
            btn.pack(side="left", padx=1)


def start_up():
    interface_support.main()
if __name__ == '__main__':
    interface_support.main()