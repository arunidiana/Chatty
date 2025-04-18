# src/chatty_app/config.py
import os

# Pfade
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Gibt das 'src' Verzeichnis
# Oder, wenn run_chatty.py außerhalb von src liegt und das Projekt-Root das Arbeitsverzeichnis ist:
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Projekt-Root
# Sicherer: Den Pfad explizit übergeben oder relativ zum Skript im scripts-Ordner machen
# Für jetzt nehmen wir an, der assets-Ordner liegt eine Ebene über src/
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'assets'))
LOGO_PATH = os.path.join(ASSETS_DIR, "Logo.png")


# Farben
BG_COLOR = "#C7FAF9"
FG_COLOR = "#1E1E1E"
ACCENT_COLOR = "#007AFF"
EXIT_COLOR = "#A9A9A9"
ENTRY_BG_COLOR = "#FFFFFF"
TEXT_AREA_BG = BG_COLOR
BUBBLE_COLOR = "#FFFFFF"
BUBBLE_FG = "#1E1E1E"
ERROR_BUBBLE_BG = "#FFF0F0"
ERROR_BUBBLE_FG = "#D8000C"
SEPARATOR_COLOR = "#CCCCCC"

# Schriftarten und Größen
FONT_FAMILY = "Segoe UI"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 11
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 18

# Layout & Größen
LOGO_SIZE = (150, 150)
TOP_BAR_LOGO_SIZE = (120, 120)
SEPARATOR_LENGTH = 30 # Länge der Trennlinie

# Gemini Konfiguration
INITIAL_HISTORY = [
     {
            "role": "user",
            "parts": [
                "Hallo Chatty! Für unser Gespräch gilt: Du bist ein freundlicher Chatbot, der sich ausschließlich auf lockere, alltägliche Unterhaltung konzentriert. "
                "Bitte vermeide es, Code zu schreiben, komplexe Probleme zu lösen, detaillierte technische Erklärungen zu geben oder spezifische Anweisungen auszuführen, die über eine normale Unterhaltung hinausgehen. "
                "Wenn du nach solchen Dingen gefragt wirst, weise bitte höflich darauf hin, dass du nur zum Plaudern da bist. Halte deine Antworten gesprächig und freundlich."
            ]
        },
        {
            "role": "model",
            "parts": [
                "Hallo! Ich bin Chatty und freue mich auf eine nette, lockere Unterhaltung mit dir. "
                "Worüber möchtest du gerne quatschen?"
            ]
        }
]

# API Key Handling (Laden direkt hier, um es zentral zu haben)
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '..', '.env')) # Suche .env im Projekt-Root
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")