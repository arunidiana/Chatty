# src/chatty_app/main_app.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox # Für Fehlermeldungen
from . import config
from . import gui_utils
from . import ui_components
from . import gemini_interface

class ChattyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatty")
        self.root.geometry("550x650")
        self.root.config(bg=config.BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing) # Handle window close

        # Konfiguriere Styles
        gui_utils.configure_styles()

        # Initialisiere Gemini (oder prüfe zumindest Key)
        if not config.GOOGLE_API_KEY:
             messagebox.showerror("Fehler", "GOOGLE_API_KEY nicht gefunden.\nÜberprüfe die .env-Datei im Projekt-Root.")
             self.root.quit()
             return

        # Initialisiere Widget-Referenzen
        self.chat_window = None
        self.entry = None
        self.send_button = None
        self.exit_button = None

        # Erstelle die Frames
        self.start_frame = ui_components.create_start_frame(self.root, self._show_chat_screen)
        chat_widgets = ui_components.create_chat_frame(self.root, self._show_start_screen, self._send_message_command)

        self.chat_main_frame = chat_widgets["main_frame"]
        self.chat_window = chat_widgets["chat_window"]
        self.entry = chat_widgets["entry"]
        self.send_button = chat_widgets["send_button"]
        self.exit_button = chat_widgets["exit_button"]

        # Zeige initial die Startseite
        self._show_start_screen()

    def _show_start_screen(self):
        """Zeigt den Startbildschirm an."""
        self.chat_main_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title("Chatty - Start")

    def _show_chat_screen(self):
        """Initialisiert Gemini und zeigt den Chat-Bildschirm an."""
        success, error_msg = gemini_interface.initialize_gemini()
        if not success:
            messagebox.showerror("Gemini Fehler", error_msg)
            # Bleibe auf dem Startbildschirm oder beende
            # self.root.quit() # Oder nur return
            return

        self.start_frame.pack_forget()
        self.chat_main_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title("Chatty - Konversation")

        # Leere Fenster und füge erste Nachricht ein
        self.chat_window.config(state='normal')
        self.chat_window.delete('1.0', tk.END)
        self.chat_window.config(state='disabled')
        if config.INITIAL_HISTORY and len(config.INITIAL_HISTORY) > 1 and config.INITIAL_HISTORY[1]['role'] == 'model':
            gui_utils.insert_bubble(self.chat_window, "Chatty: " + config.INITIAL_HISTORY[1]['parts'][0], "bot_bubble", is_first_message=True)

        self.entry.focus()

    def _send_message_command(self):
        """Wird aufgerufen, wenn der Senden-Button geklickt oder Enter gedrückt wird."""
        user_input = self.entry.get()
        if user_input.strip() == "":
            return

        gui_utils.insert_bubble(self.chat_window, "Du: " + user_input, "user_bubble")
        self.entry.delete(0, tk.END)

        # UI blockieren
        self._set_chat_ui_state('disabled')

        # Nachricht an Gemini senden (im Hintergrund wäre besser für lange Antworten)
        success, response_or_error = gemini_interface.send_message_to_gemini(user_input)

        if success:
            gui_utils.insert_bubble(self.chat_window, "Chatty: " + response_or_error, "bot_bubble")
        else:
            gui_utils.insert_bubble(self.chat_window, f"Chatty Fehler: {response_or_error}", "error_bubble")

        # UI wieder freigeben
        self._set_chat_ui_state('normal')

    def _set_chat_ui_state(self, state):
        """Aktiviert oder deaktiviert die Eingabeelemente im Chat."""
        self.entry.config(state=state)
        self.send_button.config(state=state)
        self.exit_button.config(state=state)
        if state == 'normal':
            self.entry.focus()
        self.root.update_idletasks()

    def _on_closing(self):
        """Aufräumen beim Schließen des Fensters."""
        print("Anwendung wird geschlossen.")
        # Hier könnten z.B. laufende Prozesse beendet werden
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Startet die Tkinter Hauptschleife."""
        self.root.mainloop()