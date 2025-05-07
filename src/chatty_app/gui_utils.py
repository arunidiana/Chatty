# src/chatty_app/gui_utils.py
import os
from PIL import Image
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt # <-- Fehlenden Import hinzufügen

from . import config

def load_image(path, size):
    """Lädt ein Bild, skaliert es und gibt ein QPixmap-Objekt zurück."""
    try:
        if os.path.exists(path):
            # Öffne mit Pillow (obwohl wir es hier nicht direkt zur Konvertierung nutzen)
            # Es könnte für andere Prüfungen nützlich sein
            # img_pil = Image.open(path)

            # Erstelle QPixmap direkt aus dem originalen Pfad
            pixmap = QPixmap(path)
            if pixmap.isNull(): # Prüfen, ob das Laden fehlgeschlagen ist
                 print(f"Warnung: QPixmap konnte Bild nicht laden von {path}")
                 return None

            # Skaliere QPixmap unter Beibehaltung des Seitenverhältnisses mit Qt-Konstanten
            return pixmap.scaled(size[0], size[1],
                                 Qt.AspectRatioMode.KeepAspectRatio, # Jetzt verfügbar
                                 Qt.TransformationMode.SmoothTransformation) # Jetzt verfügbar
        else:
            print(f"Warnung: Bilddatei nicht gefunden unter {path}")
            return None
    except ImportError:
        # Pillow Import wird nicht mehr direkt für die Konvertierung benötigt, aber lassen wir es drin
        print("Fehler: Pillow fehlt (oder PyQt6). 'pip install Pillow PyQt6'.")
        return None
    except Exception as e:
        print(f"Fehler beim Laden/Skalieren des Bildes {path}: {e}")
        return None

# Die anderen Funktionen (configure_tags, configure_styles, insert_bubble)
# sind nicht mehr in dieser Datei, da ihre Logik in PyQt anders gehandhabt wird
# (Stylesheets in main_app, HTML-Einfügung in main_app).
# Lasse sie weg oder kommentiere sie aus, falls noch vorhanden.