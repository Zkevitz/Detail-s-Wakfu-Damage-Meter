import json
import os
from pathlib import Path

class UserPreferences:
    def __init__(self, app_name="MonApp"):
        # Dossier utilisateur (ex: ~/.mon_app/)
        self.app_dir = Path(os.path.expanduser("~")) / f".{app_name.lower()}"
        self.app_dir.mkdir(exist_ok=True)

        # Fichier JSON des préférences
        self.file_path = self.app_dir / "preferences.json"

        # Valeurs par défaut
        self.defaults = {
            "theme": "dark",
            "language": "fr",
            "window_width": 900,
            "window_height": 600,
            "show_tips": True
        }

        # Dictionnaire principal
        self.data = self.defaults.copy()

        # Charger les valeurs sauvegardées s’il existe
        self.load()

    def load(self):
        """Charge les préférences depuis le fichier s’il existe."""
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    self.data.update(saved_data)
            except Exception as e:
                print("⚠️ Erreur de chargement des préférences :", e)

    def save(self):
        """Sauvegarde les préférences dans le fichier JSON."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print("⚠️ Erreur de sauvegarde des préférences :", e)

    def get(self, key, default=None):
        """Récupère une préférence."""
        return self.data.get(key, default if default is not None else self.defaults.get(key))

    def set(self, key, value):
        """Modifie une préférence et la sauvegarde automatiquement."""
        self.data[key] = value
        self.save()

    def reset(self):
        """Réinitialise toutes les préférences à leurs valeurs par défaut."""
        self.data = self.defaults.copy()
        self.save()