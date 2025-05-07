# src/chatty_app/main_app.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from firebase_admin import firestore # <-- Import für SERVER_TIMESTAMP hinzufügen
from . import config
from . import gui_utils
from . import ui_components
from . import gemini_interface
from . import firebase_logger
# from . import firebase_auth # <-- Entfernen

class ChattyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatty - Login")
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
             messagebox.showwarning("Firebase Fehler", f"Firebase nicht initialisiert:\n{fb_error}\nAuthentifizierung und Logging sind deaktiviert.")

        # Widget-Referenzen
        self.chat_window = None
        self.entry = None
        self.send_button = None
        self.exit_button = None
        self.username_entry = None
        self.password_entry = None
        self.login_button = None
        self.register_button = None

        # Zustand
        self.current_user = None
        self.current_user_id = None # Optional, aber kann ID speichern

        # Erstelle die Frames
        start_widgets = ui_components.create_start_frame(self.root, self._login_clicked, self._register_clicked)
        self.start_frame = start_widgets["start_frame"]
        self.username_entry = start_widgets["username_entry"]
        self.password_entry = start_widgets["password_entry"]
        self.login_button = start_widgets["login_button"]
        self.register_button = start_widgets["register_button"]
        

        chat_widgets = ui_components.create_chat_frame(self.root, self._show_start_screen, self._send_message_command)
        self.chat_main_frame = chat_widgets["main_frame"]
        self.chat_window = chat_widgets["chat_window"]
        self.entry = chat_widgets["entry"]
        self.send_button = chat_widgets["send_button"]
        self.exit_button = chat_widgets["exit_button"]

        self._show_start_screen()

    # --- HIER AUTH-Methoden integrieren ---

    def _sanitize_username_for_id(self, username):
        """Bereinigt einen Benutzernamen, um als Firestore Dokument-ID gültig zu sein."""
        # (Identisch wie in firebase_auth.py)
        sanitized = username.lower().replace(" ", "_").replace(".", "_dot_").replace("@", "_at_")
        sanitized = "".join(c for c in sanitized if c.isalnum() or c == '_')
        if not sanitized:
            return None
        return sanitized

    def _register_user(self, username, password):
        """Registriert einen neuen Benutzer mit Klartext-Passwort direkt hier."""
        db = firebase_logger.get_db_client() # Hole DB Client
        if not db:
            return False, "Datenbank nicht initialisiert.", None
        if not username or not password:
            return False, "Benutzername und Passwort dürfen nicht leer sein.", None

        user_doc_id = self._sanitize_username_for_id(username)
        if not user_doc_id:
             return False, "Ungültiger Benutzername (nach Bereinigung leer).", None

        user_ref = db.collection(config.FIREBASE_USERS_COLLECTION_NAME).document(user_doc_id)

        try:
            user_doc = user_ref.get()
            if user_doc.exists:
                return False, "Benutzername bereits vergeben.", None

            user_ref.set({
                'original_username': username,
                'password_plain': password, # <-- Speichere Klartext
                'first_seen': firestore.SERVER_TIMESTAMP,
                'last_seen': firestore.SERVER_TIMESTAMP
            })
            print(f"Benutzer '{username}' (ID: {user_doc_id}) erfolgreich registriert (PASSWORT UNGESCHÜTZT!).")
            return True, "Registrierung erfolgreich.", user_doc_id

        except Exception as e:
            print(f"Fehler bei der Benutzerregistrierung für '{username}': {e}")
            return False, f"Fehler bei der Registrierung: {e}", None

    def _verify_user(self, username, password):
        """Überprüft Benutzername und Klartext-Passwort direkt hier."""
        db = firebase_logger.get_db_client() # Hole DB Client
        if not db:
            return False, "Datenbank nicht initialisiert.", None
        if not username or not password:
            return False, "Benutzername und Passwort erforderlich.", None

        user_doc_id = self._sanitize_username_for_id(username)
        if not user_doc_id:
            return False, "Ungültiger Benutzername.", None

        user_ref = db.collection(config.FIREBASE_USERS_COLLECTION_NAME).document(user_doc_id)

        try:
            user_doc = user_ref.get()
            if not user_doc.exists:
                return False, "Benutzername nicht gefunden.", None

            user_data = user_doc.to_dict()
            stored_plain_password = user_data.get('password_plain')

            if not stored_plain_password:
                 print(f"WARNUNG: Kein Klartext-Passwort für Benutzer '{username}' gefunden!")
                 return False, "Interner Fehler (fehlendes Passwortfeld).", None

            if password == stored_plain_password: # Direkter Vergleich
                user_ref.update({'last_seen': firestore.SERVER_TIMESTAMP})
                print(f"Benutzer '{username}' erfolgreich verifiziert (PASSWORT UNGESCHÜTZT!).")
                original_username = user_data.get('original_username', username)
                return True, "Login erfolgreich.", original_username
            else:
                return False, "Falsches Passwort.", None

        except Exception as e:
            print(f"Fehler bei der Benutzerverifizierung für '{username}': {e}")
            return False, f"Fehler beim Login: {e}", None

    # --- ENDE integrierte Auth-Methoden ---


    def _set_login_register_state(self, state):
        """Aktiviert/Deaktiviert Buttons auf dem Startbildschirm."""
        if self.login_button: self.login_button.config(state=state)
        if self.register_button: self.register_button.config(state=state)
        if self.username_entry: self.username_entry.config(state=state)
        if self.password_entry: self.password_entry.config(state=state)
        self.root.update_idletasks()

    def _login_clicked(self):
        """Versucht, den Benutzer einzuloggen."""
        if not self.firebase_initialized:
             messagebox.showerror("Fehler", "Firebase nicht initialisiert. Login nicht möglich.")
             return

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Eingabe fehlt", "Bitte Benutzername und Passwort eingeben.")
            return

        self._set_login_register_state('disabled')
        # Rufe die interne Methode auf
        success, message, user_info = self._verify_user(username, password)
        self._set_login_register_state('normal')

        if success:
            self.current_user = user_info
            print(f"Benutzer '{self.current_user}' eingeloggt.")
            if self.firebase_initialized:
                 firebase_logger.log_to_firestore("System", "Login erfolgreich.", username=self.current_user)
            self._show_chat_screen()
        else:
            messagebox.showerror("Login Fehlgeschlagen", message)
            self.password_entry.delete(0, tk.END)

    def _register_clicked(self):
        """Versucht, einen neuen Benutzer zu registrieren."""
        if not self.firebase_initialized:
             messagebox.showerror("Fehler", "Firebase nicht initialisiert. Registrierung nicht möglich.")
             return

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Eingabe fehlt", "Bitte Benutzername und Passwort eingeben.")
            return

        self._set_login_register_state('disabled')
        # Rufe die interne Methode auf
        success, message, user_doc_id = self._register_user(username, password)
        self._set_login_register_state('normal')

        if success:
            self.current_user = username
            self.current_user_id = user_doc_id
            messagebox.showinfo("Registrierung Erfolgreich", message)
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("System", "Benutzer registriert.", username=self.current_user)
            self._show_chat_screen()
        else:
            messagebox.showerror("Registrierung Fehlgeschlagen", message)

    def _show_start_screen(self):
        # (Code unverändert)
        self.chat_main_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)
        self.root.title("Chatty - Login")
        self.current_user = None
        self.current_user_id = None
        if self.username_entry: self.username_entry.delete(0, tk.END)
        if self.password_entry: self.password_entry.delete(0, tk.END)
        if self.username_entry: self.username_entry.focus()

    def _show_chat_screen(self):
        # (Code unverändert)
        if not self.current_user:
             print("Fehler: Kein Benutzer eingeloggt, kann Chat nicht starten.")
             self._show_start_screen()
             return
        success, error_msg = gemini_interface.initialize_gemini()
        if not success:
            messagebox.showerror("Gemini Fehler", error_msg)
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("System", f"Initialisierungsfehler Gemini: {error_msg}", username=self.current_user)
            self._show_start_screen()
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
        # (Code unverändert)
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
        # (Code unverändert)
        if self.entry: self.entry.config(state=state)
        if self.send_button: self.send_button.config(state=state)
        if self.exit_button: self.exit_button.config(state=state)
        if state == 'normal' and self.entry:
            self.entry.focus()
        self.root.update_idletasks()

    def _on_closing(self):
        # (Code unverändert)
        print("Anwendung wird geschlossen.")
        username_to_log = self.current_user or "Unbekannt"
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("System", "Anwendung geschlossen.", username=username_to_log)
        self.root.quit()
        self.root.destroy()

    def run(self):
        # (Code unverändert)
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("System", "Anwendung gestartet.", username="System")
        self.root.mainloop()