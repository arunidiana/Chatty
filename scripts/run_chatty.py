# scripts/run_chatty.py
import tkinter as tk
import sys
import os

# Füge das 'src' Verzeichnis zum Python-Pfad hinzu, damit chatty_app gefunden wird
# Passe dies an, wenn deine Struktur anders ist
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Importiere die Hauptanwendungsklasse
try:
    from chatty_app.main_app import ChattyApp
except ImportError as e:
    print(f"Fehler beim Importieren der Anwendung: {e}")
    print("Stelle sicher, dass das Skript aus dem Projekt-Root-Verzeichnis ausgeführt wird oder passe den sys.path an.")
    sys.exit(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChattyApp(root)
    app.run()