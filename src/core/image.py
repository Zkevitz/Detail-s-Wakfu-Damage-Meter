import customtkinter as ctk
from PIL import Image

trashIcon = ctk.CTkImage(
    light_image=Image.open("assets/interface/delete.png"),
    dark_image=Image.open("assets/interface/delete.png"),
    size=(10, 10)
)