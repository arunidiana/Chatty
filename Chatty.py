import tkinter as tk
import google.generativeai as genai
import os                 # Importiere das os-Modul
from dotenv import load_dotenv # Importiere load_dotenv

# --- Lade Umgebungsvariablen aus der .env-Datei ---
load_dotenv()

# --- Hole den API-Key aus den Umgebungsvariablen ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Überprüfe, ob der Key geladen wurde ---
if not GOOGLE_API_KEY:
    print("Fehler: GOOGLE_API_KEY wurde nicht in der .env-Datei gefunden oder die Datei fehlt.")
    print("Stelle sicher, dass eine .env-Datei im selben Verzeichnis wie das Skript existiert")
    print("und dass sie 'GOOGLE_API_KEY=DEIN_KEY' enthält.")
    # Optional: Zeige Fehler im GUI an
    # Wichtig: root muss hier noch nicht existieren, daher besser nur print oder exit()
    # tk.messagebox.showerror("Konfigurationsfehler", "GOOGLE_API_KEY nicht gefunden.\nÜberprüfe die .env-Datei.")
    exit() # Beendet das Skript, wenn der Key fehlt

# --- Konfiguriere und initialisiere Gemini ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)

    # --- Modell initialisieren und Chat-Sitzung starten ---
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    # Startet eine Chat-Sitzung, die den Verlauf speichert
    chat = model.start_chat(history=[])
    print("Gemini-Modell und Chat-Sitzung erfolgreich initialisiert.")

except Exception as e:
    # Zeige Fehler im Terminal an, wenn die Initialisierung fehlschlägt
    print(f"Fehler bei der Initialisierung von Gemini: {e}")
    print("Stelle sicher, dass der API-Key in der .env-Datei korrekt und gültig ist.")
    # Optional: Zeige eine Fehlermeldung im GUI an statt nur zu drucken
    # Da das GUI hier vielleicht noch nicht initialisiert ist, ist print sicherer.
    # Wenn du sicherstellst, dass root initialisiert ist, kannst du messagebox verwenden.
    # try:
    #    root = tk.Tk()
    #    root.withdraw() # Verstecke das Hauptfenster für die Fehlermeldung
    #    tk.messagebox.showerror("Gemini Fehler", f"Fehler bei der Initialisierung:\n{e}\nStelle sicher, dass der API-Key in der .env-Datei korrekt ist.")
    # except tk.TclError: # Falls Tkinter nicht initialisiert werden kann
    #     pass # Fehler wurde schon in der Konsole ausgegeben
    exit() # Beendet das Skript bei Initialisierungsfehler

# --- Funktion für GUI-Nachrichtensenden ---
def send_message(event=None): # event=None für <Return>-Bindung
    user_input = entry.get()
    if user_input.strip() == "":
        return

    # Benutzer-Nachricht im Chat anzeigen
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "Du: " + user_input + "\n")
    chat_window.see(tk.END) # Nach unten scrollen
    chat_window.config(state='disabled')

    # Eingabefeld leeren
    entry.delete(0, tk.END)

    # Eingabe und Button deaktivieren, während auf Antwort gewartet wird
    entry.config(state='disabled')
    send_button.config(state='disabled')
    root.update_idletasks() # GUI aktualisieren, um Deaktivierung anzuzeigen

    # Antwort von Gemini holen (mit Konversationsverlauf)
    try:
        # Verwende die Chat-Sitzung, um die Nachricht zu senden
        # Das 'chat'-Objekt enthält den bisherigen Verlauf
        response = chat.send_message(user_input)
        response_text = response.text.strip()

    except Exception as e:
        response_text = f"Fehler mit Gemini: {e}"
        print(f"Gemini API Error: {e}") # Fehler auch im Terminal anzeigen
        # Optional: Fehlermeldung im Chatfenster anzeigen
        chat_window.config(state='normal')
        chat_window.insert(tk.END, f"Chatty Fehler: {e}\n\n")
        chat_window.see(tk.END) # Nach unten scrollen
        chat_window.config(state='disabled')
        # Eingabe/Button wieder aktivieren, damit der Nutzer es erneut versuchen kann
        entry.config(state='normal')
        send_button.config(state='normal')
        entry.focus()
        return # Keine "Chatty:" Antwort anzeigen bei Fehler

    # Chatty-Antwort im Chat anzeigen
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "Chatty: " + response_text + "\n\n")
    chat_window.see(tk.END) # Nach unten scrollen
    chat_window.config(state='disabled')

    # Eingabe und Button wieder aktivieren
    entry.config(state='normal')
    send_button.config(state='normal')
    entry.focus() # Cursor wieder ins Eingabefeld setzen


# --- GUI-Setup ---
root = tk.Tk()
root.title("Chatty (mit Gemini KI & Verlauf)")
root.geometry("500x600") # Höhe angepasst

# --- Chat-Fenster mit Scrollbar ---
chat_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(chat_frame) # Scrollbar erstellen
chat_window = tk.Text(
    chat_frame,
    state='disabled',
    wrap='word',
    bg="#F0F0F0",
    font=("Arial", 12),
    yscrollcommand=scrollbar.set # Scrollbar mit Textfenster verbinden
)
scrollbar.config(command=chat_window.yview) # Scrollbar-Aktion definieren

# Elemente im Frame platzieren
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# --- Ende Chat-Fenster ---

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=(0, 5), fill=tk.X)
# Bindet die Enter-Taste an die send_message Funktion
entry.bind("<Return>", send_message) # Event-Objekt wird übergeben

send_button = tk.Button(root, text="Senden", command=send_message)
send_button.pack(padx=10, pady=(0, 10))

# Fokus auf das Eingabefeld setzen, wenn das Fenster startet
entry.focus()

root.mainloop()