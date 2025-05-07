# src/chatty_app/firebase_logger.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
from . import config

db = None

def initialize_firebase():
    # (Code unverändert)
    global db
    if not firebase_admin._apps:
        try:
            if not os.path.exists(config.FIREBASE_SERVICE_ACCOUNT_KEY_PATH):
                 error_msg = f"Firebase Service Account Key nicht gefunden unter: {config.FIREBASE_SERVICE_ACCOUNT_KEY_PATH}"
                 print(f"Fehler: {error_msg}")
                 return False, error_msg
            cred = credentials.Certificate(config.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Firebase erfolgreich initialisiert.")
            return True, None
        except ValueError as ve:
            error_msg = f"Fehler bei Firebase-Initialisierung (ungültiger Key?): {ve}"
            print(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Allgemeiner Fehler bei Firebase-Initialisierung: {e}"
            print(error_msg)
            return False, error_msg
    else:
        if db is None:
            db = firestore.client()
        print("Firebase war bereits initialisiert.")
        return True, None

def log_to_firestore(speaker, message, username="System"):
    # (Code unverändert, verwendet jetzt config.FIREBASE_LOG_COLLECTION_NAME)
    global db
    if not db:
        print("Fehler: Firestore DB Client nicht initialisiert. Logging fehlgeschlagen.")
        return False
    try:
        log_data = {
            'speaker': speaker,
            'message': message,
            'username': username,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        collection_ref = db.collection(config.FIREBASE_LOG_COLLECTION_NAME) # Nutzt Log Collection
        collection_ref.add(log_data)
        return True
    except Exception as e:
        print(f"Fehler beim Schreiben nach Firestore in Collection '{config.FIREBASE_LOG_COLLECTION_NAME}': {e}")
        return False

def get_logs_from_firestore(limit=50):
    # (Code unverändert, verwendet jetzt config.FIREBASE_LOG_COLLECTION_NAME)
    global db
    if not db:
        print("Fehler: Firestore DB Client nicht initialisiert. Logs können nicht abgerufen werden.")
        return []
    try:
        collection_ref = db.collection(config.FIREBASE_LOG_COLLECTION_NAME) # Nutzt Log Collection
        query = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        logs = []
        for doc in docs:
            log_data = doc.to_dict()
            if 'timestamp' in log_data and hasattr(log_data['timestamp'], 'strftime'):
                 log_data['timestamp_str'] = log_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            logs.append(log_data)
        print(f"{len(logs)} Log-Einträge aus Firestore Collection '{config.FIREBASE_LOG_COLLECTION_NAME}' abgerufen.")
        return logs
    except Exception as e:
        print(f"Fehler beim Abrufen der Logs aus Firestore Collection '{config.FIREBASE_LOG_COLLECTION_NAME}': {e}")
        return []

# --- NEUE BENUTZERFUNKTIONEN ---
def _sanitize_username_for_id(username):
    """Bereinigt einen Benutzernamen, um als Firestore Dokument-ID gültig zu sein."""
    # Ähnlich wie Collection-Namen, aber hier für Dokument-IDs
    # Leerzeichen etc. durch Unterstriche ersetzen. E-Mail-Adressen könnten : enthalten.
    # Dies ist eine einfache Version.
    sanitized = username.lower().replace(" ", "_").replace(".", "_at_").replace("@", "_at_")
    # Entferne andere ungültige Zeichen (Beispiel)
    sanitized = "".join(c for c in sanitized if c.isalnum() or c == '_')
    if not sanitized:
        return "unknown_user"
    return sanitized

def add_or_update_user(username):
    """Fügt einen Benutzer zur 'users'-Collection hinzu oder aktualisiert den Zeitstempel des letzten Logins."""
    global db
    if not db:
        print("Fehler: Firestore DB Client nicht initialisiert. Benutzer kann nicht hinzugefügt/aktualisiert werden.")
        return False, None

    if not username or not username.strip():
        print("Fehler: Benutzername ist leer.")
        return False, None

    # Verwende den bereinigten Benutzernamen als Dokument-ID
    user_doc_id = _sanitize_username_for_id(username)
    user_ref = db.collection(config.FIREBASE_USERS_COLLECTION_NAME).document(user_doc_id)

    try:
        user_doc = user_ref.get()
        if user_doc.exists:
            # Benutzer existiert, aktualisiere 'last_seen'
            user_ref.update({
                'last_seen': firestore.SERVER_TIMESTAMP,
                'original_username': username # Speichere auch den originalen Namen
            })
            print(f"Benutzer '{username}' (ID: {user_doc_id}) aktualisiert.")
        else:
            # Benutzer existiert nicht, erstelle ihn
            user_ref.set({
                'original_username': username,
                'first_seen': firestore.SERVER_TIMESTAMP,
                'last_seen': firestore.SERVER_TIMESTAMP
                # Hier könnten weitere Benutzerinfos gespeichert werden
            })
            print(f"Benutzer '{username}' (ID: {user_doc_id}) zur Firestore Users-Collection hinzugefügt.")
        return True, user_doc_id
    except Exception as e:
        print(f"Fehler beim Hinzufügen/Aktualisieren des Benutzers '{username}' (ID: {user_doc_id}): {e}")
        return False, None

if __name__ == '__main__':
    print("Teste Firebase Logger und User Funktionen...")
    initialized, init_error = initialize_firebase()
    if initialized:
        print(f"\nTeste Logging in Collection '{config.FIREBASE_LOG_COLLECTION_NAME}':")
        log_to_firestore("System", "Test-Log-Eintrag gestartet.")

        test_user = "Max Mustermann"
        test_user_email = "max.mustermann@example.com"

        print(f"\nTeste Benutzer hinzufügen/aktualisieren für '{test_user}':")
        success_user, user_id = add_or_update_user(test_user)
        if success_user:
            log_to_firestore("User", "Meine Testnachricht.", username=test_user)
            log_to_firestore("Bot", "Meine Testantwort.", username=test_user)

        print(f"\nTeste Benutzer hinzufügen/aktualisieren für '{test_user_email}':")
        success_email_user, email_user_id = add_or_update_user(test_user_email)
        if success_email_user:
             log_to_firestore("User", "Eine andere Nachricht.", username=test_user_email)


        print(f"\nTeste Log-Abruf aus Collection '{config.FIREBASE_LOG_COLLECTION_NAME}':")
        retrieved_logs = get_logs_from_firestore(10)
        for log in reversed(retrieved_logs):
             ts = log.get('timestamp_str', log.get('timestamp', 'N/A'))
             print(f"[{ts}] {log.get('username','System')}/{log.get('speaker', 'N/A')}: {log.get('message', 'N/A')}")
    else:
        print(f"Initialisierung fehlgeschlagen: {init_error}")