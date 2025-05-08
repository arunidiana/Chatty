# src/chatty_app/main_app.py
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox, QStackedWidget,
    QTextEdit, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor
from html import escape
try:
    from . import config
    from . import gui_utils
    from . import ui_components_qt as ui_components
    from . import gemini_interface
    from . import firebase_logger
    from firebase_admin import firestore
except ImportError as e:
    print(f"Import-Fehler in main_app.py: {e}")
    sys.exit(1)

class ChattyApp(QMainWindow):
    def __init__(self, root=None):
        super().__init__()

        self.current_user = None
        self.current_user_id = None

        self.firebase_initialized, fb_error = firebase_logger.initialize_firebase()
        if not self.firebase_initialized:
             QTimer.singleShot(100, lambda: QMessageBox.warning(self, "Firebase Fehler", f"Firebase nicht initialisiert:\n{fb_error}\nAuthentifizierung und Logging sind deaktiviert."))

        if not config.GOOGLE_API_KEY:
             QMessageBox.critical(None, "Fehler", "GOOGLE_API_KEY nicht gefunden.\nÜberprüfe die .env-Datei im Projekt-Root.")
             QTimer.singleShot(0, sys.exit)
             return

        self.setWindowTitle("Chatty")
        self.setGeometry(200, 200, 550, 650)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.start_screen_widgets = None
        self.chat_screen_widgets = None
        self.username_entry: QLineEdit | None = None
        self.password_entry: QLineEdit | None = None
        self.login_button: QPushButton | None = None
        self.register_button: QPushButton | None = None
        self.chat_window: QTextEdit | None = None
        self.entry: QLineEdit | None = None
        self.send_button: QPushButton | None = None
        self.exit_button: QPushButton | None = None

        self._create_ui()
        self._apply_styles()

        self._show_start_screen()

    def _create_ui(self):
        self.start_screen_widgets = ui_components.create_start_widget(
            login_callback=self._login_clicked,
            register_callback=self._register_clicked
        )
        self.stacked_widget.addWidget(self.start_screen_widgets["main_widget"])

        self.chat_screen_widgets = ui_components.create_chat_widget(
            back_callback=self._show_start_screen,
            send_callback=self._send_message_command
        )
        self.stacked_widget.addWidget(self.chat_screen_widgets["main_widget"])

        self.username_entry = self.start_screen_widgets.get("username_entry")
        self.password_entry = self.start_screen_widgets.get("password_entry")
        self.login_button = self.start_screen_widgets.get("login_button")
        self.register_button = self.start_screen_widgets.get("register_button")
        self.chat_window = self.chat_screen_widgets.get("chat_window")
        self.entry = self.chat_screen_widgets.get("entry")
        self.send_button = self.chat_screen_widgets.get("send_button")
        self.exit_button = self.chat_screen_widgets.get("exit_button")

        if self.entry:
            self.entry.returnPressed.connect(self._send_message_command)

    def _apply_styles(self):
        stylesheet = f"""
            QWidget {{
                font-family: "{config.FONT_FAMILY}";
                color: {config.FG_COLOR};
            }}
            QMainWindow {{
                background-color: {config.BG_COLOR};
            }}
            QPushButton#LoginButton, QPushButton#RegisterButton {{
                font-size: {config.FONT_SIZE_LARGE}pt; font-weight: bold; padding: 15px;
                background-color: {config.ACCENT_COLOR}; color: {config.ENTRY_BG_COLOR};
                border: none; border-radius: 5px;
            }}
            QPushButton#LoginButton:hover, QPushButton#RegisterButton:hover {{ background-color: #0056b3; }}
            QPushButton#LoginButton:pressed, QPushButton#RegisterButton:pressed {{ background-color: #004085; }}
            QPushButton#BackButton {{
                font-size: {config.FONT_SIZE_SMALL}pt; padding: 5px;
                background-color: {config.EXIT_COLOR}; color: {config.ENTRY_BG_COLOR};
                border: none; border-radius: 3px;
            }}
             QPushButton#BackButton:hover {{ background-color: #808080; }}
             QPushButton#BackButton:pressed {{ background-color: #696969; }}
            QPushButton#SendButton {{
                 font-size: {config.FONT_SIZE_NORMAL}pt; font-weight: bold; padding: 8px;
                 background-color: {config.ACCENT_COLOR}; color: {config.ENTRY_BG_COLOR};
                 border: none; border-radius: 5px;
            }}
            QPushButton#SendButton:hover {{ background-color: #0056b3; }}
            QPushButton#SendButton:pressed {{ background-color: #004085; }}
            QLineEdit {{
                font-size: {config.FONT_SIZE_LARGE}pt; padding: 10px;
                background-color: {config.ENTRY_BG_COLOR};
                border: 1px solid #ccc; border-radius: 5px;
            }}
            QTextEdit#ChatWindow {{
                font-size: {config.FONT_SIZE_NORMAL}pt;
                background-color: {config.TEXT_AREA_BG};
                border: 1px solid #ccc; border-radius: 5px; padding: 10px;
            }}
            QLabel#WelcomeLabel {{
                 font-size: {config.FONT_SIZE_XLARGE}pt; font-weight: bold;
                 color: {config.FG_COLOR}; qproperty-alignment: 'AlignCenter';
            }}
        """
        self.setStyleSheet(stylesheet)

    def _sanitize_username_for_id(self, username):
        sanitized = username.lower().replace(" ", "_").replace(".", "_dot_").replace("@", "_at_")
        sanitized = "".join(c for c in sanitized if c.isalnum() or c == '_')
        if not sanitized: return None
        return sanitized

    def _register_user(self, username, password):
        db = firebase_logger.get_db_client()
        if not db: return False, "Datenbank nicht initialisiert.", None
        if not username or not password: return False, "Benutzername/Passwort leer.", None
        user_doc_id = self._sanitize_username_for_id(username)
        if not user_doc_id: return False, "Ungültiger Benutzername.", None
        user_ref = db.collection(config.FIREBASE_USERS_COLLECTION_NAME).document(user_doc_id)
        try:
            if user_ref.get().exists: return False, "Benutzername vergeben.", None
            user_ref.set({
                'original_username': username, 'password_plain': password,
                'first_seen': firestore.SERVER_TIMESTAMP, 'last_seen': firestore.SERVER_TIMESTAMP
            })
            print(f"Benutzer '{username}' registriert (PASSWORT UNGESCHÜTZT!).")
            return True, "Registrierung erfolgreich.", user_doc_id
        except Exception as e: return False, f"Fehler bei Registrierung: {e}", None

    def _verify_user(self, username, password):
        db = firebase_logger.get_db_client()
        if not db: return False, "Datenbank nicht initialisiert.", None
        if not username or not password: return False, "Benutzername/Passwort erforderlich.", None
        user_doc_id = self._sanitize_username_for_id(username)
        if not user_doc_id: return False, "Ungültiger Benutzername.", None
        user_ref = db.collection(config.FIREBASE_USERS_COLLECTION_NAME).document(user_doc_id)
        try:
            user_doc = user_ref.get()
            if not user_doc.exists: return False, "Benutzername nicht gefunden.", None
            user_data = user_doc.to_dict()
            stored_plain_password = user_data.get('password_plain')
            if not stored_plain_password: return False, "Interner Fehler (Passwortfeld fehlt).", None
            if password == stored_plain_password:
                user_ref.update({'last_seen': firestore.SERVER_TIMESTAMP})
                print(f"Benutzer '{username}' verifiziert (PASSWORT UNGESCHÜTZT!).")
                return True, "Login erfolgreich.", user_data.get('original_username', username)
            else: return False, "Falsches Passwort.", None
        except Exception as e: return False, f"Fehler beim Login: {e}", None

    def _set_login_register_state(self, enabled):
        state = bool(enabled)
        if self.login_button: self.login_button.setEnabled(state)
        if self.register_button: self.register_button.setEnabled(state)
        if self.username_entry: self.username_entry.setEnabled(state)
        if self.password_entry: self.password_entry.setEnabled(state)
        QApplication.processEvents()

    def _login_clicked(self):
        if not self.firebase_initialized:
             QMessageBox.critical(self, "Fehler", "Firebase nicht initialisiert.")
             return
        username = self.username_entry.text().strip()
        password = self.password_entry.text()
        if not username or not password:
            QMessageBox.warning(self, "Eingabe fehlt", "Bitte Benutzername und Passwort eingeben.")
            return
        self._set_login_register_state(False)
        success, message, user_info = self._verify_user(username, password)
        self._set_login_register_state(True)
        if success:
            self.current_user = user_info
            if self.firebase_initialized:
                 firebase_logger.log_to_firestore("System", "Login erfolgreich.", username=self.current_user)
            self._show_chat_screen()
        else:
            QMessageBox.critical(self, "Login Fehlgeschlagen", message)
            self.password_entry.clear()

    def _register_clicked(self):
        if not self.firebase_initialized:
             QMessageBox.critical(self, "Fehler", "Firebase nicht initialisiert.")
             return
        username = self.username_entry.text().strip()
        password = self.password_entry.text()
        if not username or not password:
            QMessageBox.warning(self, "Eingabe fehlt", "Bitte Benutzername und Passwort eingeben.")
            return
        self._set_login_register_state(False)
        success, message, user_doc_id = self._register_user(username, password)
        self._set_login_register_state(True)
        if success:
            self.current_user = username
            self.current_user_id = user_doc_id
            QMessageBox.information(self, "Registrierung Erfolgreich", message)
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("System", "Benutzer registriert.", username=self.current_user)
            self._show_chat_screen()
        else:
            QMessageBox.critical(self, "Registrierung Fehlgeschlagen", message)

    def _show_start_screen(self):
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle("Chatty - Login")
        self.current_user = None
        self.current_user_id = None
        if self.username_entry: self.username_entry.clear()
        if self.password_entry: self.password_entry.clear()
        if self.username_entry: self.username_entry.setFocus()

    def _show_chat_screen(self):
        if not self.current_user:
             print("Fehler: Kein Benutzer eingeloggt.")
             self._show_start_screen()
             return
        success, error_msg = gemini_interface.initialize_gemini()
        if not success:
            QMessageBox.critical(self, "Gemini Fehler", error_msg)
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("System", f"Initialisierungsfehler Gemini: {error_msg}", username=self.current_user)
            self._show_start_screen()
            return
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle(f"Chatty - Konversation ({self.current_user})")
        if self.chat_window:
            self.chat_window.clear()
            if config.INITIAL_HISTORY and len(config.INITIAL_HISTORY) > 1 and config.INITIAL_HISTORY[1]['role'] == 'model':
                initial_bot_message_text = config.INITIAL_HISTORY[1]['parts'][0]
                self._insert_html_bubble("Chatty: " + initial_bot_message_text, "bot")
                if self.firebase_initialized:
                     firebase_logger.log_to_firestore("Chatty", initial_bot_message_text, username=self.current_user)
        if self.entry: self.entry.setFocus()

    def _insert_html_bubble(self, full_message, speaker_type):
        if not self.chat_window: return

        speaker = "Unbekannt"
        message_text = full_message
        if ":" in full_message:
            parts = full_message.split(":", 1)
            speaker = parts[0].strip()
            message_text = parts[1].strip()

        is_user_message = (speaker_type == "user")
        if is_user_message:
            speaker = self.current_user

        background_color = config.BUBBLE_COLOR
        text_color = config.BUBBLE_FG
        alignment = "left"
        margin_left = "10px"
        margin_right = "70px"

        if is_user_message:
            alignment = "right"
            margin_left = "70px"
            margin_right = "10px"
            background_color = getattr(config, 'USER_BUBBLE_BG', config.BUBBLE_COLOR)
        elif speaker_type == "error":
             background_color = config.ERROR_BUBBLE_BG
             text_color = config.ERROR_BUBBLE_FG

        message_html = escape(message_text).replace('\n', '<br>')

        html_content = f"""
        <div style="text-align: {alignment}; margin-left: {margin_left}; margin-right: {margin_right}; margin-bottom: {getattr(config, 'BUBBLE_VERTICAL_SPACING', '10px')};">
            <div style="display: inline-block; background-color: {background_color}; color: {text_color}; padding: 8px 12px; border-radius: {getattr(config, 'BUBBLE_BORDER_RADIUS', '15px')}; text-align: left; max-width: 80%;">
                <b>{escape(speaker)}:</b><br>
                {message_html}
            </div>
        </div>
        """
        cursor = self.chat_window.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_window.setTextCursor(cursor)
        self.chat_window.insertHtml(html_content)
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_window.setTextCursor(cursor)
        self.chat_window.ensureCursorVisible()

    def _send_message_command(self):
        if not self.current_user: return
        user_input = self.entry.text().strip()
        if not user_input: return
        self._insert_html_bubble(f"Du: {user_input}", "user")
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("Du", user_input, username=self.current_user)
        self.entry.clear()
        self._set_chat_ui_state(False)
        success, response_or_error = gemini_interface.send_message_to_gemini(user_input)
        if success:
            self._insert_html_bubble("Chatty: " + response_or_error, "bot")
            if self.firebase_initialized:
                 firebase_logger.log_to_firestore("Chatty", response_or_error, username=self.current_user)
        else:
            error_display_text = f"Chatty Fehler: {response_or_error}"
            self._insert_html_bubble(error_display_text, "error")
            if self.firebase_initialized:
                firebase_logger.log_to_firestore("Fehler", response_or_error, username=self.current_user)
        self._set_chat_ui_state(True)

    def _set_chat_ui_state(self, enabled):
        state = bool(enabled)
        if self.entry: self.entry.setEnabled(state)
        if self.send_button: self.send_button.setEnabled(state)
        if self.exit_button: self.exit_button.setEnabled(state)
        if state and self.entry: self.entry.setFocus()
        QApplication.processEvents()

    def closeEvent(self, event):
        self._on_closing()
        event.accept()

    def _on_closing(self):
        print("Anwendung wird geschlossen.")
        username_to_log = self.current_user or "Unbekannt"
        if self.firebase_initialized:
            firebase_logger.log_to_firestore("System", "Anwendung geschlossen.", username=username_to_log)