# src/chatty_app/firebase_logger.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
from . import config

db = None

def initialize_firebase():
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
        collection_ref = db.collection(config.FIREBASE_COLLECTION_NAME)
        collection_ref.add(log_data)
        return True
    except Exception as e:
        print(f"Fehler beim Schreiben nach Firestore: {e}")
        return False

def get_logs_from_firestore(limit=50):
    global db
    if not db:
        print("Fehler: Firestore DB Client nicht initialisiert. Logs können nicht abgerufen werden.")
        return []
    try:
        collection_ref = db.collection(config.FIREBASE_COLLECTION_NAME)
        query = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        logs = []
        for doc in docs:
            log_data = doc.to_dict()
            if 'timestamp' in log_data and hasattr(log_data['timestamp'], 'strftime'):
                 log_data['timestamp_str'] = log_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            logs.append(log_data)
        print(f"{len(logs)} Log-Einträge aus Firestore abgerufen.")
        return logs
    except Exception as e:
        print(f"Fehler beim Abrufen der Logs aus Firestore: {e}")
        return []

if __name__ == '__main__':
    print("Teste Firebase Logger...")
    initialized, init_error = initialize_firebase()
    if initialized:
        print("\nTeste Logging:")
        log_to_firestore("System", "Test-Log-Eintrag gestartet.")
        log_to_firestore("User", "Meine Testnachricht.", username="TestUser")
        log_to_firestore("Bot", "Meine Testantwort.", username="TestUser")
        print("\nTeste Log-Abruf:")
        retrieved_logs = get_logs_from_firestore(5)
        for log in reversed(retrieved_logs):
             ts = log.get('timestamp_str', log.get('timestamp', 'N/A'))
             print(f"[{ts}] {log.get('username','System')}/{log.get('speaker', 'N/A')}: {log.get('message', 'N/A')}")
    else:
        print(f"Initialisierung fehlgeschlagen: {init_error}")