# src/chatty_app/main_app.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from . import config
from . import gui_utils
from . import ui_components
from . import gemini_interface
from . import firebase_logger

class ChattyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatty")
        self.root.geometry("550x650")
        self.root.config(bg=config.BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        gui_utils.configure_styles()

        if not config.GOOGLE_API_KEY:
             messagebox.showerror("Fehler", "GOOGLE_API_KEY nicht gefunden.")
             self.root.quit()
             return

        self.firebase_initialized, fb_error = firebase_logger.initialize_firebase()
        if not self.firebase_initialized:
             messagebox.showwarning("Firebase Fehler", f"Firebase nicht initialisiert:\n{fb_error}\nLogging ist deaktiviert.")

        self.chat_window = None
        self.entry = None
        self.send_button = None
        self.exit_button = None
        self.username_entry = None
        self.current_user = None

        self.start_frame, self.username_entry = ui_components.create_start_frame(self.root, self._start_chat_button_clicked)

        chat_widgets = ui_components.create_chat_frame(self.root, self._show_start_screen, self._send_message_command)
        self.chat_main_frame = chat_widgets["main_frame"]
        self.chat_window = chat_widgets["chat_window"]
        self.entry = chat_widgets["entry"]
        self.send_button = chat_widgets["send_button"]
        self.exit_button = chat_widgets["exit_button"]

        self._show_start_screen()

    def _start_chat_button_clicked(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Eingabe fehlt", "Bitte gib deinen Namen ein.")
            return
        self.current_user = username
        print(f"Benutzer '{self.current_user}' startet den Chat.")
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("System", f"Chat gestartet", username=self.current_user)
        self._show_chat_screen()

    def _show_start_screen(self):
        self.chat_main_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title("Chatty - Start")
        self.current_user = None
        if self.username_entry:
            self.username_entry.delete(0, tk.END)

    def _show_chat_screen(self):
        if not self.current_user:
             print("Fehler: Kein Benutzer gesetzt, kann Chat nicht starten.")
             self._show_start_screen()
             return

        success, error_msg = gemini_interface.initialize_gemini()
        if not success:
            messagebox.showerror("Gemini Fehler", error_msg)
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("System", f"Initialisierungsfehler Gemini: {error_msg}", username=self.current_user)
            return

        self.start_frame.pack_forget()
        self.chat_main_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title(f"Chatty - Konversation ({self.current_user})")

        self.chat_window.config(state='normal')
        self.chat_window.delete('1.0', tk.END)
        self.chat_window.config(state='disabled')

        if config.INITIAL_HISTORY and len(config.INITIAL_HISTORY) > 1 and config.INITIAL_HISTORY[1]['role'] == 'model':
            initial_bot_message_text = config.INITIAL_HISTORY[1]['parts'][0]
            gui_utils.insert_bubble(self.chat_window, "Chatty: " + initial_bot_message_text, "bot_bubble", is_first_message=True)
            if self.firebase_initialized:
                 firebase_logger.log_to_firestore("Chatty", initial_bot_message_text, username=self.current_user)

        self.entry.focus()

    def _send_message_command(self):
        if not self.current_user:
             print("Fehler: Kein Benutzer für das Senden der Nachricht vorhanden.")
             return

        user_input = self.entry.get().strip()
        if not user_input:
            return

        gui_utils.insert_bubble(self.chat_window, f"Du: {user_input}", "user_bubble", username=self.current_user)
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("Du", user_input, username=self.current_user)
        self.entry.delete(0, tk.END)

        self._set_chat_ui_state('disabled')

        success, response_or_error = gemini_interface.send_message_to_gemini(user_input)

        if success:
            gui_utils.insert_bubble(self.chat_window, "Chatty: " + response_or_error, "bot_bubble")
            if self.firebase_initialized:
                 firebase_logger.log_to_firestore("Chatty", response_or_error, username=self.current_user)
        else:
            error_display_text = f"Chatty Fehler: {response_or_error}"
            gui_utils.insert_bubble(self.chat_window, error_display_text, "error_bubble")
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("Fehler", response_or_error, username=self.current_user)

        self._set_chat_ui_state('normal')

    def _set_chat_ui_state(self, state):
        if self.entry: self.entry.config(state=state)
        if self.send_button: self.send_button.config(state=state)
        if self.exit_button: self.exit_button.config(state=state)
        if state == 'normal' and self.entry:
            self.entry.focus()
        self.root.update_idletasks()

    def _on_closing(self):
        print("Anwendung wird geschlossen.")
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("System", "Anwendung geschlossen.", username=self.current_user or "Unbekannt")
        self.root.quit()
        self.root.destroy()

    def run(self):
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("System", "Anwendung gestartet.", username="System")
        self.root.mainloop()