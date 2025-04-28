# src/chatty_app/main_app.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        gui_utils.configure_styles()

        if not config.GOOGLE_API_KEY:
             messagebox.showerror("Fehler", "GOOGLE_API_KEY nicht gefunden.\nÜberprüfe die .env-Datei im Projekt-Root.")
             self.root.quit()
             return

        self.chat_window = None
        self.entry = None
        self.send_button = None
        self.exit_button = None

        self.start_frame = ui_components.create_start_frame(self.root, self._show_chat_screen)
        chat_widgets = ui_components.create_chat_frame(self.root, self._show_start_screen, self._send_message_command)

        self.chat_main_frame = chat_widgets["main_frame"]
        self.chat_window = chat_widgets["chat_window"]
        self.entry = chat_widgets["entry"]
        self.send_button = chat_widgets["send_button"]
        self.exit_button = chat_widgets["exit_button"]

        self._show_start_screen()

    def _show_start_screen(self):
        self.chat_main_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title("Chatty - Start")

    def _show_chat_screen(self):
        success, error_msg = gemini_interface.initialize_gemini()
        if not success:
            messagebox.showerror("Gemini Fehler", error_msg)
            gui_utils.log_message("System", f"Initialisierungsfehler: {error_msg}")
            return

        self.start_frame.pack_forget()
        self.chat_main_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title("Chatty - Konversation")

        self.chat_window.config(state='normal')
        self.chat_window.delete('1.0', tk.END)
        self.chat_window.config(state='disabled')

        if config.INITIAL_HISTORY and len(config.INITIAL_HISTORY) > 1 and config.INITIAL_HISTORY[1]['role'] == 'model':
            initial_bot_message = "Chatty: " + config.INITIAL_HISTORY[1]['parts'][0]
            gui_utils.insert_bubble(self.chat_window, initial_bot_message, "bot_bubble", is_first_message=True)
            gui_utils.log_message("Chatty", config.INITIAL_HISTORY[1]['parts'][0])

        self.entry.focus()

    def _send_message_command(self):
        user_input = self.entry.get()
        if user_input.strip() == "":
            return

        gui_utils.insert_bubble(self.chat_window, "Du: " + user_input, "user_bubble")
        gui_utils.log_message("Du", user_input)
        self.entry.delete(0, tk.END)

        self._set_chat_ui_state('disabled')

        success, response_or_error = gemini_interface.send_message_to_gemini(user_input)

        if success:
            gui_utils.insert_bubble(self.chat_window, "Chatty: " + response_or_error, "bot_bubble")
            gui_utils.log_message("Chatty", response_or_error)
        else:
            error_display_text = f"Chatty Fehler: {response_or_error}"
            gui_utils.insert_bubble(self.chat_window, error_display_text, "error_bubble")
            gui_utils.log_message("Fehler", response_or_error)

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
        gui_utils.log_message("System", "Anwendung geschlossen.")
        self.root.quit()
        self.root.destroy()

    def run(self):
        gui_utils.log_message("System", "Anwendung gestartet.")
        self.root.mainloop()