# src/chatty_app/firebase_logger.py
import firebase_admin
from firebase_admin import credentials, firestore
import os
from . import config # Für Pfad zur Schlüsseldatei und Collection-Namen

# Modul-interne Variable für den Firestore DB Client
db = None

def initialize_firebase():
    """Initialisiert die Firebase Admin SDK Verbindung und den Firestore Client."""
    global db
    # Verhindere erneute Initialisierung
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
            # Oftmals Problem mit dem Key-Format
            error_msg = f"Fehler bei Firebase-Initialisierung (ungültiger Key?): {ve}"
            print(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Allgemeiner Fehler bei Firebase-Initialisierung: {e}"
            print(error_msg)
            return False, error_msg
    else:
        # Bereits initialisiert, stelle sicher, dass db gesetzt ist
        if db is None:
            db = firestore.client()
        print("Firebase war bereits initialisiert.")
        return True, None

def log_to_firestore(speaker, message):
    """Schreibt eine Chat-Nachricht als Dokument in die Firestore-Sammlung."""
    global db
    if not db:
        print("Fehler: Firestore DB Client nicht initialisiert. Logging fehlgeschlagen.")
        return False

    try:
        # Daten für das Firestore-Dokument
        log_data = {
            'speaker': speaker,
            'message': message,
            'timestamp': firestore.SERVER_TIMESTAMP # Nutzt den Server-Zeitstempel
        }
        # Füge ein neues Dokument mit automatisch generierter ID hinzu
        collection_ref = db.collection(config.FIREBASE_COLLECTION_NAME)
        collection_ref.add(log_data)
        # print(f"Logged to Firestore: {speaker}: {message[:50]}...") # Optional: Debug-Ausgabe
        return True
    except Exception as e:
        print(f"Fehler beim Schreiben nach Firestore: {e}")
        return False

def get_logs_from_firestore(limit=50):
    """Ruft die letzten 'limit' Log-Einträge aus Firestore ab (optional)."""
    global db
    if not db:
        print("Fehler: Firestore DB Client nicht initialisiert. Logs können nicht abgerufen werden.")
        return []

    try:
        collection_ref = db.collection(config.FIREBASE_COLLECTION_NAME)
        # Nach Zeitstempel absteigend sortieren, um die neuesten zuerst zu bekommen
        query = collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()

        logs = []
        for doc in docs:
            log_data = doc.to_dict()
            # Konvertiere Firestore Timestamp zu lesbarem Format (optional)
            if 'timestamp' in log_data and hasattr(log_data['timestamp'], 'strftime'):
                 log_data['timestamp_str'] = log_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            logs.append(log_data)

        print(f"{len(logs)} Log-Einträge aus Firestore abgerufen.")
        return logs
    except Exception as e:
        print(f"Fehler beim Abrufen der Logs aus Firestore: {e}")
        return []

# Beispielaufruf (nur zum Testen dieses Moduls direkt, wird von main_app nicht verwendet)
if __name__ == '__main__':
    print("Teste Firebase Logger...")
    initialized, init_error = initialize_firebase()
    if initialized:
        print("\nTeste Logging:")
        log_to_firestore("System", "Test-Log-Eintrag gestartet.")
        log_to_firestore("User", "Meine Testnachricht.")
        log_to_firestore("Bot", "Meine Testantwort.")

        print("\nTeste Log-Abruf:")
        retrieved_logs = get_logs_from_firestore(5)
        for log in reversed(retrieved_logs): # In chronologischer Reihenfolge ausgeben
             ts = log.get('timestamp_str', log.get('timestamp', 'N/A'))
             print(f"[{ts}] {log.get('speaker', 'N/A')}: {log.get('message', 'N/A')}")
    else:
        print(f"Initialisierung fehlgeschlagen: {init_error}")