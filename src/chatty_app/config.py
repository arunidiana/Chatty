# src/chatty_app/config.py
import os

# --- Pfade ---
# Definiere das Projekt-Root-Verzeichnis (eine Ebene über dem 'src'-Verzeichnis)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
LOGO_PATH = os.path.join(ASSETS_DIR, "Logo.png")
# LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "log.txt") # Alte lokale Log-Datei, nicht mehr primär genutzt

# --- Firebase Konfiguration --- NEU ---
FIREBASE_SERVICE_ACCOUNT_KEY_PATH = os.path.join(PROJECT_ROOT, "firebase-service-account.json") # Pfad zur Schlüsseldatei
FIREBASE_COLLECTION_NAME = "chat_logs" # Name der Sammlung in Firestore

# --- Farben ---
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

# --- Schriftarten und Größen ---
FONT_FAMILY = "Segoe UI"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 11
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 18

# --- Layout & Größen ---
LOGO_SIZE = (150, 150)
# TOP_BAR_LOGO_SIZE war im Ausgangscode 120x120, im Firebase-Beispiel 30x30. Ich nehme 30x30 an.
TOP_BAR_LOGO_SIZE = (30, 30)
SEPARATOR_LENGTH = 30 # Länge der Trennlinie

# --- Gemini Konfiguration ---
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

# --- API Key Handling ---
from dotenv import load_dotenv
# Suche .env im Projekt-Root
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")