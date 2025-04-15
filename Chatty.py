import tkinter as tk
from tkinter import ttk
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk # Importiere Pillow Module

# --- Lade Umgebungsvariablen ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Globale Variable für Chat-Objekt ---
chat = None
initial_history = [
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

# --- Funktion zum Initialisieren von Gemini (unverändert) ---
def initialize_gemini():
    global chat, initial_history
    if not GOOGLE_API_KEY:
        print("Fehler: GOOGLE_API_KEY nicht gefunden. Überprüfe die .env-Datei.")
        root.quit()
        return False
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        chat = model.start_chat(history=initial_history[:])
        print("Gemini-Modell und Chat-Sitzung erfolgreich initialisiert/zurückgesetzt.")
        return True
    except Exception as e:
        print(f"Fehler bei der Initialisierung von Gemini: {e}")
        print("Stelle sicher, dass der API-Key in der .env-Datei korrekt und gültig ist.")
        root.quit()
        return False

# --- Funktion zum Anzeigen der Chat-Oberfläche (unverändert) ---
def show_chat_screen():
    if not initialize_gemini():
        print("Initialisierung fehlgeschlagen. Chat kann nicht gestartet werden.")
        return
    start_frame.pack_forget()
    chat_main_frame.pack(fill=tk.BOTH, expand=True)
    chat_window.config(state='normal')
    chat_window.delete('1.0', tk.END)
    chat_window.config(state='disabled')
    # Füge die *erste* Nachricht ohne vorherige Trennlinie ein
    if chat and initial_history and len(initial_history) > 1 and initial_history[1]['role'] == 'model':
         insert_bubble(chat_window, "Chatty: " + initial_history[1]['parts'][0], "bot_bubble", is_first_message=True)
    entry.focus()

# --- Funktion zum Anzeigen der Startseite (unverändert) ---
def show_start_screen():
    chat_main_frame.pack_forget()
    start_frame.pack(fill=tk.BOTH, expand=True)

# --- Hilfsfunktion zum Einfügen von Blasen ---
# Hinzugefügt: is_first_message Flag, um die erste Trennlinie zu vermeiden
# Geändert: Fügt Trennlinie *vor* der Bubble ein (außer bei der ersten)
def insert_bubble(text_widget, text, tag_name, is_first_message=False):
    text_widget.config(state='normal')

    # Füge eine Trennlinie *vor* jeder Nachricht ein, außer der allerersten
    if not is_first_message:
        # Hier wird die Trennlinie eingefügt
        # '─' ist ein Box-Drawing-Zeichen. Wiederhole es für die Breite.
        # Passe die Anzahl der Wiederholungen ggf. an die Fensterbreite an.
        separator_text = "─" * 30  # Beispiel: 60 Striche
        # Füge Leerraum über und unter der Linie durch \n ein + wende Tag an
        text_widget.insert(tk.END, f"\n{separator_text}\n\n", "separator_line")

    # Füge die eigentliche Bubble-Nachricht ein
    text_widget.insert(tk.END, text + "\n", tag_name) # Nur ein \n nach dem Text

    text_widget.config(state='disabled')
    text_widget.see(tk.END)


# --- Funktion für GUI-Nachrichtensenden ---
# Geändert: Ruft insert_bubble ohne is_first_message auf (Standard ist False)
def send_message(event=None):
    if not chat:
        print("Fehler: Chat-Objekt nicht initialisiert.")
        return
    user_input = entry.get()
    if user_input.strip() == "":
        return

    # Füge Benutzer-Bubble ein (mit Trennlinie davor)
    insert_bubble(chat_window, "Du: " + user_input, "user_bubble")
    entry.delete(0, tk.END)

    entry.config(state='disabled')
    send_button.config(state='disabled')
    exit_button.config(state='disabled')
    root.update_idletasks()

    try:
        response = chat.send_message(user_input)
        response_text = response.text.strip()
        # Füge Bot-Bubble ein (mit Trennlinie davor)
        insert_bubble(chat_window, "Chatty: " + response_text, "bot_bubble")
    except Exception as e:
        error_text = f"Fehler: {e}"
        print(f"Gemini API Error: {e}")
        # Füge Fehler-Bubble ein (mit Trennlinie davor)
        insert_bubble(chat_window, f"Chatty Fehler: {error_text}", "error_bubble")

    entry.config(state='normal')
    send_button.config(state='normal')
    exit_button.config(state='normal')
    entry.focus()

# --- GUI-Setup ---
root = tk.Tk()
root.title("Chatty")
root.geometry("550x650")

# --- Style-Definitionen ---
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
SEPARATOR_COLOR = "#CCCCCC" # Farbe für die Trennlinie (helles Grau) <-- NEU
FONT_FAMILY = "Segoe UI"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 11
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 18
# BUBBLE_PADDING nicht mehr benötigt für spacing3
LOGO_SIZE = (150, 150)
TOP_BAR_LOGO_SIZE = (120, 120) # War vorher 120x120, ggf. anpassen

# --- Hauptfenster-Styling ---
root.config(bg=BG_COLOR)

# --- ttk Style konfigurieren (unverändert) ---
style = ttk.Style()
try:
    style.theme_use('clam')
except tk.TclError:
    print("Theme 'clam' nicht verfügbar, verwende Standard-Theme.")
# Style-Definitionen für Buttons, Entry, Frame, Scrollbar (unverändert)
style.configure("TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"), padding=8, foreground=ENTRY_BG_COLOR, background=ACCENT_COLOR, borderwidth=0, relief="flat")
style.map("TButton", background=[('active', '#0056b3')])
style.configure("Exit.TButton", font=(FONT_FAMILY, FONT_SIZE_SMALL), padding=5, foreground=ENTRY_BG_COLOR, background=EXIT_COLOR, borderwidth=0, relief="flat")
style.map("Exit.TButton", background=[('active', '#808080')])
style.configure("Start.TButton", font=(FONT_FAMILY, FONT_SIZE_LARGE, "bold"), padding=15)
style.map("Start.TButton", background=[('active', '#0056b3')])
style.configure("TEntry", font=(FONT_FAMILY, FONT_SIZE_LARGE), padding=10, foreground=FG_COLOR, fieldbackground=ENTRY_BG_COLOR, borderwidth=1, relief="solid")
style.configure("TFrame", background=BG_COLOR)
style.configure("Vertical.TScrollbar", troughcolor=BG_COLOR, background=ACCENT_COLOR, borderwidth=0, arrowsize=0)
style.map("Vertical.TScrollbar", background=[('active', '#0056b3')])


# === Startseite Frame (unverändert) ===
start_frame = ttk.Frame(root, padding="20", style="TFrame")
start_frame.pack(fill=tk.BOTH, expand=True)
# --- Logo für Startseite laden und anzeigen (unverändert) ---
logo_label = None; logo_image_tk = None
try:
    script_dir = os.path.dirname(os.path.abspath(__file__)); logo_path = os.path.join(script_dir, "Logo.png")
    if os.path.exists(logo_path):
        logo_image_pil = Image.open(logo_path); logo_image_pil.thumbnail(LOGO_SIZE, Image.Resampling.LANCZOS)
        logo_image_tk = ImageTk.PhotoImage(logo_image_pil); logo_label = ttk.Label(start_frame, image=logo_image_tk, background=BG_COLOR)
        logo_label.image = logo_image_tk; logo_label.pack(pady=(20, 15))
    else: print(f"Warnung: Logo-Datei nicht gefunden unter {logo_path}")
except ImportError: print("Fehler: Pillow fehlt. 'pip install Pillow'.")
except Exception as e: print(f"Fehler beim Laden des Start-Logos: {e}")
# --- Restliche Elemente der Startseite (unverändert) ---
welcome_label = ttk.Label(start_frame, text="Willkommen bei Chatty!", font=(FONT_FAMILY, FONT_SIZE_XLARGE, "bold"), background=BG_COLOR, foreground=FG_COLOR)
welcome_label.pack(pady=(0 if logo_label else 50, 20))
info_label = ttk.Label(start_frame, text="Klicke auf 'Chat starten', um eine Unterhaltung zu beginnen.", font=(FONT_FAMILY, FONT_SIZE_LARGE), background=BG_COLOR, foreground=FG_COLOR, wraplength=400, justify=tk.CENTER)
info_label.pack(pady=(0, 30))
start_button = ttk.Button(start_frame, text="Chat starten", command=show_chat_screen, style="Start.TButton", cursor="hand2")
start_button.pack(pady=20)


# === Chat Hauptframe (wird später angezeigt) ===
chat_main_frame = ttk.Frame(root, style="TFrame")

# --- Logo für die Top-Leiste laden (unverändert) ---
top_logo_label = None; top_logo_image_tk = None
try:
    script_dir = os.path.dirname(os.path.abspath(__file__)); logo_path = os.path.join(script_dir, "Logo.png")
    if os.path.exists(logo_path):
        top_logo_image_pil = Image.open(logo_path); top_logo_image_pil.thumbnail(TOP_BAR_LOGO_SIZE, Image.Resampling.LANCZOS)
        top_logo_image_tk = ImageTk.PhotoImage(top_logo_image_pil)
except ImportError: print("Info: Pillow nicht gefunden, Top-Bar-Logo wird nicht angezeigt.")
except Exception as e: print(f"Fehler beim Laden des Top-Bar-Logos: {e}")

# --- Top-Leiste mit Grid-Layout erstellen (unverändert) ---
top_bar_frame = ttk.Frame(chat_main_frame, style="TFrame")
top_bar_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
# --- "Zurück"-Button (links) (unverändert) ---
exit_button = ttk.Button(top_bar_frame, text="Zurück", command=show_start_screen, style="Exit.TButton", cursor="hand2")
exit_button.grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')
# --- Logo (Mitte) (unverändert) ---
if top_logo_image_tk:
    top_logo_label = ttk.Label(top_bar_frame, image=top_logo_image_tk, background=BG_COLOR)
    top_logo_label.image = top_logo_image_tk
    top_logo_label.grid(row=0, column=1, pady=1, padx=(0, 85)) # Padding rechts für Linksverschiebung
# --- Grid-Spalten konfigurieren (unverändert) ---
top_bar_frame.columnconfigure(0, weight=0)
top_bar_frame.columnconfigure(1, weight=1)
top_bar_frame.columnconfigure(2, weight=0)


# --- Chat-Bereich (unverändert) ---
chat_display_frame = ttk.Frame(chat_main_frame, padding="0", style="TFrame")
chat_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 0))
scrollbar = ttk.Scrollbar(chat_display_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
chat_window = tk.Text(
    chat_display_frame, wrap=tk.WORD, state='disabled', bg=TEXT_AREA_BG, fg=FG_COLOR,
    font=(FONT_FAMILY, FONT_SIZE_NORMAL), padx=10, pady=10, yscrollcommand=scrollbar.set,
    relief="flat", borderwidth=0, highlightthickness=0
)
scrollbar.config(command=chat_window.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# --- Tag-Konfigurationen für Sprechblasen ---
# spacing3 wurde entfernt, da der Abstand jetzt durch die Trennlinie+Newlines gemacht wird
chat_window.tag_configure("user_bubble", background=BUBBLE_COLOR, foreground=BUBBLE_FG, justify=tk.RIGHT, lmargin1=80, lmargin2=80, rmargin=10, wrap=tk.WORD, borderwidth=0, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
chat_window.tag_configure("bot_bubble", background=BUBBLE_COLOR, foreground=BUBBLE_FG, justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=80, wrap=tk.WORD, borderwidth=0, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
chat_window.tag_configure("error_bubble", background=ERROR_BUBBLE_BG, foreground=ERROR_BUBBLE_FG, justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=80, wrap=tk.WORD, borderwidth=0, font=(FONT_FAMILY, FONT_SIZE_NORMAL, "italic"))

# --- NEUE Tag-Konfiguration für die Trennlinie ---
chat_window.tag_configure("separator_line",
                          foreground=SEPARATOR_COLOR, # Farbe der Linie
                          justify=tk.CENTER,          # Zentriert die Linie (falls sie kürzer als die Breite ist)
                          font=(FONT_FAMILY, FONT_SIZE_SMALL)) # Kleinere Schrift für die Linie

# --- Eingabe-Bereich (unverändert) ---
input_frame = ttk.Frame(chat_main_frame, padding="10 10 10 10", style="TFrame")
input_frame.pack(fill=tk.X, padx=10, pady=10)
entry = ttk.Entry(input_frame, font=(FONT_FAMILY, FONT_SIZE_LARGE), style="TEntry")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
entry.bind("<Return>", send_message)
send_button = ttk.Button(input_frame, text="Senden", command=send_message, style="TButton")
send_button.pack(side=tk.LEFT, padx=(10, 0))

# --- Starte die Hauptschleife ---
root.mainloop()