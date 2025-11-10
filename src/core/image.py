import customtkinter as ctk
from PIL import Image
from core.utils import resource_path

trashIcon = ctk.CTkImage(
    light_image=Image.open(resource_path("assets/interface/delete.png")),
    dark_image=Image.open(resource_path("assets/interface/delete.png")),
    size=(10, 10)
)