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
    # ... (deine initial_history - unverändert) ...
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
    global chat
    if not GOOGLE_API_KEY:
        print("Fehler: GOOGLE_API_KEY nicht gefunden. Überprüfe die .env-Datei.")
        root.quit()
        return False
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        chat = model.start_chat(history=initial_history)
        print("Gemini-Modell und Chat-Sitzung erfolgreich initialisiert.")
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
    if chat and initial_history and len(initial_history) > 1 and initial_history[1]['role'] == 'model':
         insert_bubble(chat_window, "Chatty: " + initial_history[1]['parts'][0], "bot_bubble")
    entry.focus()

# --- Hilfsfunktion zum Einfügen von Blasen (unverändert) ---
def insert_bubble(text_widget, text, tag_name):
    text_widget.config(state='normal')
    text_widget.insert(tk.END, text + "\n\n", tag_name)
    text_widget.config(state='disabled')
    text_widget.see(tk.END)

# --- Funktion für GUI-Nachrichtensenden (unverändert) ---
def send_message(event=None):
    if not chat:
        print("Fehler: Chat-Objekt nicht initialisiert.")
        return
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
root.title("Chatty")
root.geometry("550x650")

# --- Style-Definitionen (unverändert) ---
BG_COLOR = "#C7FAF9"
FG_COLOR = "#1E1E1E"
ACCENT_COLOR = "#007AFF"
ENTRY_BG_COLOR = "#FFFFFF"
TEXT_AREA_BG = BG_COLOR
BUBBLE_COLOR = "#FFFFFF"
BUBBLE_FG = "#1E1E1E"
ERROR_BUBBLE_BG = "#FFF0F0"
ERROR_BUBBLE_FG = "#D8000C"
FONT_FAMILY = "Segoe UI"
FONT_SIZE_NORMAL = 14
FONT_SIZE_LARGE = 11
FONT_SIZE_XLARGE = 18
BUBBLE_PADDING = 12
LOGO_SIZE = (240, 240) # Definiere die gewünschte Größe für das Logo (Breite, Höhe)

# --- Hauptfenster-Styling ---
root.config(bg=BG_COLOR)

# --- ttk Style konfigurieren (unverändert) ---
style = ttk.Style()
try:
    style.theme_use('clam')
except tk.TclError:
    print("Theme 'clam' nicht verfügbar, verwende Standard-Theme.")
style.configure("TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"), padding=8, foreground=ENTRY_BG_COLOR, background=ACCENT_COLOR, borderwidth=0, relief="flat")
style.map("TButton", background=[('active', '#0056b3')])
style.configure("TEntry", font=(FONT_FAMILY, FONT_SIZE_LARGE), padding=10, foreground=FG_COLOR, fieldbackground=ENTRY_BG_COLOR, borderwidth=1, relief="solid")
style.configure("TFrame", background=BG_COLOR)
style.configure("Vertical.TScrollbar", troughcolor=BG_COLOR, background=ACCENT_COLOR, borderwidth=0, arrowsize=0)
style.map("Vertical.TScrollbar", background=[('active', '#0056b3')])
style.configure("Start.TButton", font=(FONT_FAMILY, FONT_SIZE_LARGE, "bold"), padding=15)

# === Startseite Frame ===
start_frame = ttk.Frame(root, padding="20", style="TFrame")
start_frame.pack(fill=tk.BOTH, expand=True)

# --- Logo laden und anzeigen ---
logo_label = None
logo_image_tk = None

try:
    script_dir = os.path.dirname(__file__)
    logo_path = os.path.join(script_dir, "Logo.png")

    if os.path.exists(logo_path):
        logo_image_pil = Image.open(logo_path)

        # Ändere die Größe unter Beibehaltung des Seitenverhältnisses
        # Das Bild wird so skaliert, dass es in die LOGO_SIZE (z.B. 120x120) passt,
        # ohne verzerrt zu werden. Die resultierende Größe kann kleiner sein
        # als LOGO_SIZE in einer Dimension.
        logo_image_pil.thumbnail(LOGO_SIZE, Image.Resampling.LANCZOS) # <-- HIER IST DIE ÄNDERUNG!

        logo_image_tk = ImageTk.PhotoImage(logo_image_pil)
        logo_label = ttk.Label(start_frame, image=logo_image_tk, background=BG_COLOR)
        logo_label.image = logo_image_tk # Wichtig: Referenz behalten!
        logo_label.pack(pady=(20, 15))
    else:
        print(f"Warnung: Logo-Datei nicht gefunden unter {logo_path}")

except ImportError:
    print("Fehler: Pillow-Bibliothek nicht gefunden. Bitte installiere sie mit 'pip install Pillow'.")
except Exception as e:
    print(f"Fehler beim Laden des Logos: {e}")



# --- Restliche Elemente der Startseite ---
welcome_label = ttk.Label(
    start_frame, text="Willkommen bei Chatty!",
    font=(FONT_FAMILY, FONT_SIZE_XLARGE, "bold"), background=BG_COLOR, foreground=FG_COLOR
)
# Passe pady an, je nachdem ob das Logo geladen wurde
welcome_label.pack(pady=(0 if logo_label else 50, 20)) # Weniger Abstand oben, wenn Logo da ist

info_label = ttk.Label(
    start_frame, text="Klicke auf 'Chat starten', um eine Unterhaltung zu beginnen.",
    font=(FONT_FAMILY, FONT_SIZE_LARGE), background=BG_COLOR, foreground=FG_COLOR,
    wraplength=400, justify=tk.CENTER
)
info_label.pack(pady=(0, 30)) # Etwas weniger Abstand unten

start_button = ttk.Button(
    start_frame, text="Chat starten", command=show_chat_screen,
    style="Start.TButton", cursor="hand2"
)
start_button.pack(pady=20)


# === Chat Hauptframe (enthält Chat und Eingabe - unverändert) ===
chat_main_frame = ttk.Frame(root, style="TFrame")
chat_display_frame = ttk.Frame(chat_main_frame, padding="0", style="TFrame")
chat_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
scrollbar = ttk.Scrollbar(chat_display_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
chat_window = tk.Text(
    chat_display_frame, wrap=tk.WORD, state='disabled', bg=TEXT_AREA_BG, fg=FG_COLOR,
    font=(FONT_FAMILY, FONT_SIZE_LARGE), padx=10, pady=10, yscrollcommand=scrollbar.set,
    relief="flat", borderwidth=0, highlightthickness=0
)
scrollbar.config(command=chat_window.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Tags (unverändert)
bubble_internal_padx = 8
bubble_internal_pady = 5
chat_window.tag_configure("user_bubble", background=BUBBLE_COLOR, foreground=BUBBLE_FG, justify=tk.RIGHT, lmargin1=80, lmargin2=80, rmargin=10, spacing3=BUBBLE_PADDING, wrap=tk.WORD, borderwidth=0, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
chat_window.tag_configure("bot_bubble", background=BUBBLE_COLOR, foreground=BUBBLE_FG, justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=80, spacing3=BUBBLE_PADDING, wrap=tk.WORD, borderwidth=0, font=(FONT_FAMILY, FONT_SIZE_NORMAL))
chat_window.tag_configure("error_bubble", background=ERROR_BUBBLE_BG, foreground=ERROR_BUBBLE_FG, justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=80, spacing3=BUBBLE_PADDING, wrap=tk.WORD, borderwidth=0, font=(FONT_FAMILY, FONT_SIZE_NORMAL, "italic"))

# Eingabe (unverändert)
input_frame = ttk.Frame(chat_main_frame, padding="10 10 10 10", style="TFrame")
input_frame.pack(fill=tk.X, padx=10, pady=10)
entry = ttk.Entry(input_frame, font=(FONT_FAMILY, FONT_SIZE_LARGE), style="TEntry")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
entry.bind("<Return>", send_message)
send_button = ttk.Button(input_frame, text="Senden", command=send_message, style="TButton")
send_button.pack(side=tk.LEFT, padx=(10, 0))

# --- Starte die Hauptschleife ---
root.mainloop()