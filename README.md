# Chatty - Einfacher Gemini Chatbot mit Tkinter und Firebase Logging

Dies ist eine Desktop-Chat-Anwendung mit einer grafischen Benutzeroberfläche (GUI), erstellt mit Python und Tkinter. Sie ermöglicht es Benutzern, mit dem Google Gemini Pro 1.5 KI-Modell zu interagieren und speichert den Chatverlauf persistent in einer Google Firebase Firestore-Datenbank.

Die Anwendung verfügt über eine Startseite und eine separate Chat-Ansicht. Sensible Informationen wie der Google API Key und der Firebase Service Account Key werden sicher über Umgebungsvariablen bzw. separate, ignorierte Dateien verwaltet.

**(Optional: Füge hier einen Screenshot der Anwendung ein)**
`[Screenshot Placeholder - füge hier ein Bild der laufenden Anwendung ein]`

## ✨ Features

*   **Grafische Benutzeroberfläche (GUI):** Einfache und benutzerfreundliche Oberfläche mit Start- und Chat-Bildschirm, erstellt mit Tkinter und ttk für ein moderneres Aussehen.
*   **Google Gemini Integration:** Nutzt das `gemini-1.5-pro-latest` Modell für intelligente Antworten.
*   **Firebase Firestore Logging:** Speichert den gesamten Chatverlauf (Benutzer, Bot, Systemnachrichten, Fehler) persistent in einer Cloud Firestore-Datenbank.
*   **Sicheres Management von Zugangsdaten:**
    *   Verwendet `python-dotenv` zum Laden des Google API-Schlüssels aus einer `.env`-Datei.
    *   Nutzt eine Service Account JSON-Datei für die Firebase-Authentifizierung (muss manuell heruntergeladen und gesichert werden).
*   **Strukturierter Code:** Aufgeteilt in Module für Konfiguration, GUI-Hilfsfunktionen, UI-Komponenten, Gemini-Interaktion und Firebase-Logging innerhalb eines `src`-Layouts.
*   **Einfache Bedienung:** Nachrichten senden via Eingabefeld/Button/Enter, Navigation zwischen Start- und Chat-Ansicht.
*   **Visuelles Feedback:** Trennlinien zwischen Chat-Nachrichten für bessere Lesbarkeit.

## ⚙️ Voraussetzungen

Bevor du beginnst, stelle sicher, dass du Folgendes eingerichtet und installiert hast:

1.  **Python 3.x:** Lade es von [python.org](https://www.python.org/) herunter.
2.  **pip:** Der Python-Paketmanager (normalerweise mit Python installiert).
3.  **Tkinter:** Ist meistens standardmäßig enthalten. Ggf. nachinstallieren (`sudo apt-get install python3-tk` unter Debian/Ubuntu).
4.  **Git:** (Optional, zum Klonen des Repositories).
5.  **Google Gemini API Key:** Erhältlich über das [Google AI Studio](https://aistudio.google.com/app/apikey).
6.  **Firebase Projekt:**
    *   Ein Google Firebase Projekt ([console.firebase.google.com](https://console.firebase.google.com/)).
    *   **Firestore Datenbank:** Im Projekt aktiviert (Native-Modus). Wähle einen Speicherort.
    *   **Firebase Service Account Key:** Eine JSON-Schlüsseldatei für dein Projekt.

## 🚀 Installation & Setup

1.  **Klone das Repository (oder lade die Dateien herunter):**
    ```bash
    git clone <URL_deines_Repositories> # Ersetze dies ggf.
    cd <Projektverzeichnis>
    ```
    Oder lade die ZIP-Datei herunter und entpacke sie. Wechsle in das Hauptverzeichnis des Projekts.

2.  **Erstelle eine virtuelle Umgebung (dringend empfohlen):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Installiere die benötigten Python-Bibliotheken:**
    ```bash
    pip install -r requirements.txt
    ```
    (Stelle sicher, dass `requirements.txt` existiert und `google-generativeai`, `python-dotenv`, `Pillow`, `firebase-admin` enthält. Falls nicht, installiere sie manuell: `pip install google-generativeai python-dotenv Pillow firebase-admin`)

4.  **Richte Firebase ein:**
    *   Gehe zu deiner Firebase-Konsole -> Projekteinstellungen -> Dienstkonten.
    *   Klicke auf "Neuen privaten Schlüssel generieren" und bestätige.
    *   Eine JSON-Datei wird heruntergeladen. **Benenne diese Datei in `firebase-service-account.json` um.**
    *   **Platziere die Datei `firebase-service-account.json` im Hauptverzeichnis deines Projekts** (auf derselben Ebene wie die Ordner `src`, `scripts`, `assets`).
    *   **WICHTIG:** Diese Datei enthält sensible Zugangsdaten!

5.  **Richte den Google API Key ein:**
    *   Erstelle im **Hauptverzeichnis** deines Projekts eine Datei namens `.env`.
    *   Füge die folgende Zeile hinzu und ersetze den Platzhalter durch deinen Key:
        ```dotenv
        # .env Datei
        GOOGLE_API_KEY=DEIN_ECHTER_GOOGLE_API_SCHLÜSSEL_HIER
        ```

6.  **Konfiguriere `.gitignore` (SEHR WICHTIG!):**
    *   Stelle sicher, dass deine `.gitignore`-Datei im Hauptverzeichnis existiert.
    *   Füge die folgenden Zeilen hinzu (oder stelle sicher, dass sie vorhanden sind), um sensible Dateien und generierte Ordner zu ignorieren:
        ```gitignore
        # .gitignore Datei
        .env
        firebase-service-account.json
        venv/
        __pycache__/
        *.pyc
        # Ggf. alte log.txt ignorieren
        log.txt
        ```

## ▶️ Anwendung starten

Führe das Startskript aus dem **Hauptverzeichnis (Projekt-Root)** deines Projekts aus:

```bash
python scripts/run_chatty.py