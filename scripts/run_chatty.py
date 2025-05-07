# scripts/run_chatty.py
import sys
import os
from PyQt6.QtWidgets import QApplication

# Füge das 'src' Verzeichnis zum Python-Pfad hinzu
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Importiere die Hauptanwendungsklasse
try:
    # Stelle sicher, dass du die PyQt-Version importierst
    from chatty_app.main_app import ChattyApp
except ImportError as e:
    print(f"Fehler beim Importieren der Anwendung: {e}")
    print("Stelle sicher, dass das Skript aus dem Projekt-Root ausgeführt wird.")
    print("Stelle sicher, dass alle Module im 'chatty_app' Ordner vorhanden sind.")
    print("Stelle sicher, dass PyQt6 installiert ist ('pip install PyQt6').")
    sys.exit(1)
except Exception as e:
    print(f"Ein unerwarteter Fehler ist beim Import aufgetreten: {e}")
    sys.exit(1)


if __name__ == "__main__":
    # Erstelle die QApplication Instanz
    app = QApplication(sys.argv)

    # Erstelle das Hauptfenster (unsere ChattyApp Klasse)
    # Der __init__ von ChattyApp wird hier ausgeführt
    try:
        main_window = ChattyApp()
    except Exception as e:
        # Fange Fehler ab, die während __init__ auftreten könnten
        # (z.B. wenn eine Datei fehlt und kritisch ist)
        print(f"Fehler während der Initialisierung der ChattyApp: {e}")
        # Zeige Fehler auch grafisch, falls möglich (QMessageBox braucht eine laufende App)
        # Oft ist es besser, kritische Fehler vor app.exec() zu behandeln
        from PyQt6.QtWidgets import QMessageBox # Lokaler Import für den Notfall
        QMessageBox.critical(None, "Initialisierungsfehler", f"Konnte die Anwendung nicht initialisieren:\n{e}")
        sys.exit(1)


    # --- WICHTIG: Zeige das Fenster an ---
    main_window.show()

    # --- Starte die Event-Schleife von Qt ---
    sys.exit(app.exec())