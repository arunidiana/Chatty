# src/chatty_app/gemini_interface.py
import google.generativeai as genai
from . import config

chat_session = None

def initialize_gemini():
    global chat_session
    if not config.GOOGLE_API_KEY:
        print("Fehler: GOOGLE_API_KEY nicht gefunden.")
        return False, "API-Key nicht gefunden. Überprüfe die .env-Datei."
    try:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        chat_session = model.start_chat(history=config.INITIAL_HISTORY[:])
        print("Gemini-Modell und Chat-Sitzung erfolgreich initialisiert.")
        return True, None
    except Exception as e:
        error_msg = f"Fehler bei der Initialisierung von Gemini: {e}"
        print(error_msg)
        print("Stelle sicher, dass der API-Key gültig ist.")
        chat_session = None
        return False, error_msg

def send_message_to_gemini(user_input):
    global chat_session
    if not chat_session:
        return False, "Chat-Sitzung nicht initialisiert."
    try:
        response = chat_session.send_message(user_input)
        return True, response.text.strip()
    except Exception as e:
        error_msg = f"Fehler bei der Kommunikation mit Gemini: {e}"
        print(f"Gemini API Error: {e}")
        return False, error_msg