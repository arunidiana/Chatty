import tkinter as tk
from tkinter import ttk
# import tkinter.messagebox # Entfernt
import google.generativeai as genai
import os
from dotenv import load_dotenv
# import textwrap # Entfernt

# --- Lade Umgebungsvariablen ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Fehler: GOOGLE_API_KEY nicht gefunden. Überprüfe die .env-Datei.")
    exit()

# --- Konfiguriere und initialisiere Gemini ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    initial_history = [
        # ... (deine initial_history von vorher - unverändert) ...
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
                "Hallo, ich bin Chatty und freue mich auf eine nette, lockere Unterhaltung mit dir. "
                "Ich werde mich aufs Plaudern konzentrieren und komplexere Anfragen oder Code-Generierung vermeiden. "
                "Worüber möchtest du gerne quatschen?"
            ]
        }
    ]
    chat = model.start_chat(history=initial_history)
    print("Gemini-Modell und Chat-Sitzung (eingeschränkt auf Konversation) erfolgreich initialisiert.")

except Exception as e:
    print(f"Fehler bei der Initialisierung von Gemini: {e}")
    print("Stelle sicher, dass der API-Key in der .env-Datei korrekt und gültig ist.")
    exit()

# --- Hilfsfunktion zum Einfügen von Blasen ---
def insert_bubble(text_widget, text, tag_name):
    text_widget.config(state='normal')
    # Füge Text + eine Leerzeile (für Abstand) mit Tag ein
    text_widget.insert(tk.END, text + "\n\n", tag_name)
    text_widget.config(state='disabled')
    text_widget.see(tk.END)

# --- Funktion für GUI-Nachrichtensenden ---
def send_message(event=None):
    user_input = entry.get()
    if user_input.strip() == "":
        return

    insert_bubble(chat_window, "Du: " + user_input, "user_bubble")

    entry.delete(0, tk.END)
    entry.config(state='disabled')
    send_button.config(state='disabled')
    root.update_idletasks()

    try:
        response = chat.send_message(user_input)
        response_text = response.text.strip()
        insert_bubble(chat_window, "Chatty: " + response_text, "bot_bubble")

    except Exception as e:
        error_text = f"Fehler: {e}"
        print(f"Gemini API Error: {e}")
        insert_bubble(chat_window, f"Chatty Fehler: {error_text}", "error_bubble")

    entry.config(state='normal')
    send_button.config(state='normal')
    entry.focus()

# --- GUI-Setup ---
root = tk.Tk()
root.title("Chatty (Konversation)")
root.geometry("550x650")

# --- Style-Definitionen ---
BG_COLOR = "#C7FAF9"       # Dein gewünschter Hintergrund
FG_COLOR = "#1E1E1E"       # Dunkler Text
ACCENT_COLOR = "#007AFF"
ENTRY_BG_COLOR = "#FFFFFF"
TEXT_AREA_BG = BG_COLOR    # Textbereich hat jetzt auch den Haupt-Hintergrund

# --- Farben für die Blasen ---
BUBBLE_COLOR = "#FFFFFF"   # Weiß für normale Blasen
BUBBLE_FG = "#1E1E1E"      # Textfarbe in den Blasen
ERROR_BUBBLE_BG = "#FFF0F0" # Sehr helles Rot für Fehlerblasen
ERROR_BUBBLE_FG = "#D8000C"

FONT_FAMILY = "Segoe UI"
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 11
BUBBLE_PADDING = 12        # Vertikaler Abstand zwischen den Blasen (ersetzt spacing3)

# --- Hauptfenster-Styling ---
root.config(bg=BG_COLOR)

# --- ttk Style konfigurieren ---
style = ttk.Style()
try:
    style.theme_use('clam')
except tk.TclError:
    print("Theme 'clam' nicht verfügbar, verwende Standard-Theme.")

# Style für TButton, TEntry, TFrame, TScrollbar (unverändert von vorher)
style.configure("TButton",
                font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
                padding=8, foreground=ENTRY_BG_COLOR, background=ACCENT_COLOR,
                borderwidth=0, relief="flat")
style.map("TButton", background=[('active', '#0056b3')])
style.configure("TEntry",
                font=(FONT_FAMILY, FONT_SIZE_LARGE), padding=10, foreground=FG_COLOR,
                fieldbackground=ENTRY_BG_COLOR, borderwidth=1, relief="solid")
style.configure("TFrame", background=BG_COLOR)
style.configure("Vertical.TScrollbar", troughcolor=BG_COLOR, background=ACCENT_COLOR, borderwidth=0, arrowsize=0)
style.map("Vertical.TScrollbar", background=[('active', '#0056b3')])

# --- Chat-Bereich ---
# Frame mit Außenabstand
chat_frame = ttk.Frame(root, padding="0", style="TFrame")
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

scrollbar = ttk.Scrollbar(chat_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")

chat_window = tk.Text(
    chat_frame,
    wrap=tk.WORD,
    state='disabled',
    bg=TEXT_AREA_BG,      # Hintergrund des gesamten Textbereichs
    fg=FG_COLOR,
    font=(FONT_FAMILY, FONT_SIZE_LARGE),
    padx=10,              # Horizontaler Innenabstand für den Textbereich
    pady=10,              # Vertikaler Innenabstand
    yscrollcommand=scrollbar.set,
    relief="flat",        # Kein Rahmen um den Textbereich selbst
    borderwidth=0,
    highlightthickness=0
)
scrollbar.config(command=chat_window.yview)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# --- Tag-Konfigurationen für Sprechblasen ---
# Hinweis: Keine runden Ecken möglich mit Text-Tags. Wir verwenden keinen Rahmen.

# Gemeinsame Optionen für Blasen-Padding (Innenabstand)
bubble_internal_padx = 8
bubble_internal_pady = 5

# Benutzer-Blase (rechts)
chat_window.tag_configure("user_bubble",
                          background=BUBBLE_COLOR,
                          foreground=BUBBLE_FG,
                          justify=tk.RIGHT,
                          lmargin1=80,  # Schiebt nach rechts
                          lmargin2=80,
                          rmargin=10,   # Rechter Abstand zum Rand
                          spacing3=BUBBLE_PADDING, # Vertikaler Abstand NACH der Blase
                          wrap=tk.WORD,
                          # Keine runden Ecken: relief=tk.FLAT (Standard) und borderwidth=0
                          borderwidth=0,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                          # Innenabstand der Blase (simuliert durch Rand um den Text)
                          # Wichtig: Funktioniert nur gut mit wrap=NONE, daher nicht ideal
                          # Besser: Text leicht einrücken, siehe unten bei `insert_bubble` (optional)
                          # oder padx/pady im Text-Widget global setzen.
                          )

# Bot-Blase (links)
chat_window.tag_configure("bot_bubble",
                          background=BUBBLE_COLOR,
                          foreground=BUBBLE_FG,
                          justify=tk.LEFT,
                          lmargin1=10,   # Linker Abstand zum Rand
                          lmargin2=10,
                          rmargin=80,   # Schiebt nach links
                          spacing3=BUBBLE_PADDING, # Vertikaler Abstand NACH der Blase
                          wrap=tk.WORD,
                          borderwidth=0,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                          )

# Fehler-Blase (links, andere Farbe)
chat_window.tag_configure("error_bubble",
                          background=ERROR_BUBBLE_BG,
                          foreground=ERROR_BUBBLE_FG,
                          justify=tk.LEFT,
                          lmargin1=10,
                          lmargin2=10,
                          rmargin=80,
                          spacing3=BUBBLE_PADDING,
                          wrap=tk.WORD,
                          borderwidth=0,
                          font=(FONT_FAMILY, FONT_SIZE_NORMAL, "italic"))

# --- Eingabe-Bereich ---
input_frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry = ttk.Entry(input_frame, font=(FONT_FAMILY, FONT_SIZE_LARGE), style="TEntry")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
entry.bind("<Return>", send_message)

send_button = ttk.Button(input_frame, text="Senden", command=send_message, style="TButton")
send_button.pack(side=tk.LEFT, padx=(10, 0))

entry.focus()

# --- Zeige die initiale "Nachricht" des Bots im Chatfenster als Blase an ---
if initial_history and len(initial_history) > 1 and initial_history[1]['role'] == 'model':
    insert_bubble(chat_window, "Chatty: " + initial_history[1]['parts'][0], "bot_bubble")

root.mainloop()