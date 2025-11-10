"""
Interface Overlay pour Wakfu Damage Meter
Utilise PyWebView pour créer un overlay transparent avec HTML/CSS
"""
import webview
import json
from threading import Thread
import time


class OverlayAPI:
    """API exposée au JavaScript pour communication bidirectionnelle"""
    
    def __init__(self, damage_tracker):
        self.tracker = damage_tracker
        self.window = None
        
    def set_window(self, window):
        """Permet de mettre à jour l'UI depuis Python"""
        self.window = window
    
    def get_combat_stats(self):
        """Retourne les stats du combat en cours"""
        if not self.tracker or not hasattr(self.tracker, 'players'):
            return []
        
        stats = []
        for player in self.tracker.players.values():
            stats.append({
                'name': player.name,
                'class': player.breed,
                'damage': player.TotalAmountOfDamage,
                'healing': player.TotalAmountOfHeal,
                'shielding': player.TotalAmountOfShield,
                'dps': player.calculate_dps() if hasattr(player, 'calculate_dps') else 0
            })
        
        # Tri par dégâts décroissants
        stats.sort(key=lambda x: x['damage'], reverse=True)
        return stats
    
    def get_combat_info(self):
        """Retourne les infos générales du combat"""
        if not self.tracker:
            return {
                'in_combat': False,
                'duration': 0,
                'TotalAmountOfDamage': 0,
                'TotalAmountOfHeal': 0
            }
        
        return {
            'in_combat': getattr(self.tracker, 'in_combat', False),
            'duration': getattr(self.tracker, 'combat_duration', 0),
            'TotalAmountOfDamage': sum(p.TotalAmountOfDamage for p in self.tracker.players.values()) if hasattr(self.tracker, 'players') else 0,
            'TotalAmountOfHeal': sum(p.TotalAmountOfHeal for p in self.tracker.players.values()) if hasattr(self.tracker, 'players') else 0
        }
    
    def reset_combat(self):
        """Réinitialise le combat"""
        if self.tracker and hasattr(self.tracker, 'reset'):
            self.tracker.reset()
            return True
        return False
    
    def get_history(self):
        """Retourne l'historique des combats"""
        if not self.tracker or not hasattr(self.tracker, 'combat_history'):
            return []
        
        return self.tracker.combat_history
    
    def toggle_lock(self):
        """Toggle le verrouillage de la fenêtre"""
        # Cette fonctionnalité sera gérée côté JS
        return True
    
    def close_app(self):
        """Ferme l'application"""
        if self.window:
            self.window.destroy()


def update_ui_loop(api, window):
    """Boucle qui met à jour l'UI périodiquement"""
    while True:
        try:
            # Envoie les nouvelles données au frontend toutes les 500ms
            stats = api.get_combat_stats()
            info = api.get_combat_info()
            
            # Utilise evaluate_js pour envoyer les données au JS
            window.evaluate_js(f'updateStats({json.dumps(stats)})')
            window.evaluate_js(f'updateCombatInfo({json.dumps(info)})')
            
            time.sleep(0.5)  # Update toutes les 500ms
        except Exception as e:
            print(f"Erreur dans update_ui_loop: {e}")
            time.sleep(1)


def start_overlay(damage_tracker):
    """
    Lance l'interface overlay
    
    Args:
        damage_tracker: Instance de votre tracker de dégâts existant
    """
    # Créer l'API
    api = OverlayAPI(damage_tracker)
    
    # Créer la fenêtre overlay
    window = webview.create_window(
        'Wakfu Damage Meter',
        'web/index.html',
        width=450,
        height=650,
        x=100,
        y=100,
        frameless=True,      # Pas de bordures Windows
        on_top=True,         # Toujours au-dessus
        transparent=True,    # Transparence activée
        easy_drag=False,     # Désactivé car géré en CSS
        resizable=False,
        js_api=api          # Expose l'API Python au JS
    )
    
    api.set_window(window)
    
    # Lance la boucle de mise à jour en arrière-plan
    update_thread = Thread(target=update_ui_loop, args=(api, window), daemon=True)
    update_thread.start()
    
    # Démarre l'application (bloquant)
    webview.start(debug=True)  # debug=False en production


if __name__ == "__main__":
    class MockTracker:
        def __init__(self):
            self.players = {}
            self.in_combat = False
            self.combat_duration = 0
    
    mock_tracker = MockTracker()
    print(f"{mock_tracker}")
    start_overlay(mock_tracker)