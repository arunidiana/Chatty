# Chatty - Einfacher Gemini Chatbot mit Tkinter

Dies ist eine einfache Desktop-Chat-Anwendung mit einer grafischen Benutzeroberfläche (GUI), die mit Python und Tkinter erstellt wurde. Sie ermöglicht es Benutzern, mit dem Google Gemini Pro 1.5 KI-Modell zu interagieren. Die Anwendung speichert den Gesprächsverlauf innerhalb einer Sitzung, um kontextbezogene Antworten zu ermöglichen.

Der API-Schlüssel für Google Gemini wird sicher über eine `.env`-Datei verwaltet, um zu verhindern, dass sensible Informationen direkt im Code stehen.

**(Optional: Füge hier einen Screenshot der Anwendung ein)**
`[Screenshot Placeholder - füge hier ein Bild der laufenden Anwendung ein]`

## ✨ Features

*   **Grafische Benutzeroberfläche (GUI):** Einfache und benutzerfreundliche Oberfläche, erstellt mit Tkinter.
*   **Google Gemini Integration:** Nutzt das `gemini-1.5-pro-latest` Modell für intelligente Antworten.
*   **Gesprächsverlauf:** Merkt sich den bisherigen Chatverlauf innerhalb einer Sitzung für kohärente Konversationen.
*   **Sicheres API-Key-Management:** Verwendet `python-dotenv` zum Laden des API-Schlüssels aus einer `.env`-Datei, anstatt ihn fest im Code zu verankern.
*   **Einfache Bedienung:** Nachrichten können über ein Eingabefeld und einen "Senden"-Button oder durch Drücken der Enter-Taste gesendet werden.
*   **Feedback bei Fehlern:** Zeigt Fehlermeldungen im Terminal an, wenn die API-Initialisierung oder die Kommunikation mit Gemini fehlschlägt.

## ⚙️ Voraussetzungen

Bevor du beginnst, stelle sicher, dass du Folgendes installiert hast:

*   **Python 3.x:** Lade es von [python.org](https://www.python.org/) herunter, falls noch nicht geschehen.
*   **pip:** Der Python-Paketmanager (wird normalerweise mit Python installiert).
*   **Tkinter:** Ist in den meisten Python-Distributionen standardmäßig enthalten. Falls nicht, muss es möglicherweise separat installiert werden (abhängig vom Betriebssystem).
*   **Google Gemini API Key:** Du benötigst einen API-Schlüssel von Google. Du kannst einen über das [Google AI Studio](https://aistudio.google.com/app/apikey) erhalten.

## 🚀 Installation & Setup

1.  **Klone das Repository (oder lade die Dateien herunter):**
    ```bash
    git clone <URL_deines_Repositories> # Ersetze dies ggf.
    cd <Verzeichnisname_des_Projekts>
    ```
    Oder lade die `.py`-Datei einfach herunter.

2.  **Installiere die benötigten Python-Bibliotheken:**
    ```bash
    pip install google-generativeai python-dotenv
    ```

3.  **Konfiguriere deinen API-Schlüssel:**
    *   Erstelle im **selben Verzeichnis** wie dein Python-Skript (z.B. `chat_app.py`) eine neue Datei mit dem Namen `.env`.
    *   Öffne die `.env`-Datei und füge die folgende Zeile hinzu, wobei du `DEIN_ECHTER_GOOGLE_API_SCHLÜSSEL_HIER` durch deinen tatsächlichen API-Schlüssel ersetzt:
        ```dotenv
        # .env Datei
        GOOGLE_API_KEY=DEIN_ECHTER_GOOGLE_API_SCHLÜSSEL_HIER
        ```
    *   **WICHTIG:** Füge die `.env`-Datei zu deiner `.gitignore`-Datei hinzu, um sicherzustellen, dass dein API-Schlüssel **niemals** in ein Git-Repository hochgeladen wird!
        ```gitignore
        # .gitignore Datei
        .env
        __pycache__/
        *.pyc
        ```

## ▶️ Anwendung starten

Führe das Python-Skript von deinem Terminal aus:

```bash
python dein_skript_name.py