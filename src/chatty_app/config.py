# src/chatty_app/config.py
import os
from dotenv import load_dotenv

# --- Pfade (unverändert) ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
LOGO_PATH = os.path.join(ASSETS_DIR, "Logo.png")
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.path.join(PROJECT_ROOT, "firebase-service-account.json")
FIREBASE_LOG_COLLECTION_NAME = "chat_logs"
FIREBASE_USERS_COLLECTION_NAME = "users"

# --- Farben (unverändert) ---
BG_COLOR = "#C7FAF9"
FG_COLOR = "#1E1E1E"
ACCENT_COLOR = "#007AFF"
EXIT_COLOR = "#A9A9A9"
ENTRY_BG_COLOR = "#FFFFFF"
TEXT_AREA_BG = BG_COLOR
BUBBLE_COLOR = "#FFFFFF" # Standard-Blasenfarbe
USER_BUBBLE_BG = "#E1FECF" # Helles Grün für Benutzer (optional)
BUBBLE_FG = "#1E1E1E"
ERROR_BUBBLE_BG = "#FFF0F0"
ERROR_BUBBLE_FG = "#D8000C"
SEPARATOR_COLOR = "#CCCCCC" # Nicht mehr für Linie, aber evtl. für Ränder?

# --- Schriftarten und Größen (unverändert) ---
FONT_FAMILY = "Segoe UI"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 11
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 18

# --- Layout & Größen ---
LOGO_SIZE = (150, 150)
TOP_BAR_LOGO_SIZE = (30, 30)
# SEPARATOR_LENGTH = 30 # Nicht mehr benötigt

# --- NEUE Bubble Styling Konstanten ---
BUBBLE_BORDER_RADIUS = "60px" # Radius für abgerundete Ecken
BUBBLE_VERTICAL_SPACING = "100px" # Abstand zwischen den Bubbles (ersetzt die Linie)

# --- Gemini Konfiguration (unverändert) ---
INITIAL_HISTORY = [
     { # ... (History Inhalt unverändert) ...
            "role": "user",
            "parts": [
                "Hallo Chatty! Für unser Gespräch gilt: Du bist ein freundlicher Chatbot, der sich ausschließlich auf lockere, alltägliche Unterhaltung konzentriert. Bitte vermeide es, Code zu schreiben, komplexe Probleme zu lösen, detaillierte technische Erklärungen zu geben oder spezifische Anweisungen auszuführen, die über eine normale Unterhaltung hinausgehen. Wenn du nach solchen Dingen gefragt wirst, weise bitte höflich darauf hin, dass du nur zum Plaudern da bist. Halte deine Antworten gesprächig und freundlich."
            ]
        },
        {
            "role": "model",
            "parts": [
                "Hallo! Ich bin Chatty und freue mich auf eine nette, lockere Unterhaltung mit dir. Worüber möchtest du gerne quatschen?"
            ]
        }
]

# --- API Key Handling (unverändert) ---
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")