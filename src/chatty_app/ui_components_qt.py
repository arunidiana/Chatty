# src/chatty_app/ui_components_qt.py
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QScrollArea, QSizePolicy, QFrame # QScrollArea nicht unbedingt nötig für QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap # Für QPixmap Typ-Hinweis, optional
from . import config
from . import gui_utils # Für load_image

def create_start_widget(login_callback, register_callback):
    """Erstellt das Start/Login-Widget (QWidget) mit PyQt6."""
    main_widget = QWidget() # Das Haupt-Container-Widget für diesen Bildschirm
    main_layout = QVBoxLayout(main_widget) # Vertikales Hauptlayout
    main_layout.setContentsMargins(20, 20, 20, 20) # Außenabstand
    main_layout.setSpacing(10) # Abstand zwischen Widgets im Layout

    # --- Logo ---
    logo_pixmap = gui_utils.load_image(config.LOGO_PATH, config.LOGO_SIZE)
    if logo_pixmap:
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setMinimumSize(config.LOGO_SIZE[0], config.LOGO_SIZE[1]) # Mindestgröße
        main_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignCenter) # Zentriert hinzufügen
        main_layout.addSpacing(15) # Abstand nach Logo

    # --- Willkommenstext ---
    welcome_label = QLabel("Willkommen bei Chatty!")
    welcome_label.setObjectName("WelcomeLabel") # Für spezifisches Styling
    # Styling wird über Stylesheet in main_app gemacht, aber Alignment hier:
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(welcome_label)
    main_layout.addSpacing(10)

    # --- Benutzername ---
    username_label = QLabel("Benutzername:")
    username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    main_layout.addWidget(username_label)

    username_entry = QLineEdit()
    username_entry.setPlaceholderText("Benutzernamen eingeben") # Platzhalter
    main_layout.addWidget(username_entry)
    main_layout.addSpacing(10)

    # --- Passwort ---
    password_label = QLabel("Passwort:")
    password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    main_layout.addWidget(password_label)

    password_entry = QLineEdit()
    password_entry.setPlaceholderText("Passwort eingeben")
    password_entry.setEchoMode(QLineEdit.EchoMode.Password) # Sternchen anzeigen
    main_layout.addWidget(password_entry)
    main_layout.addSpacing(20)

    # --- Buttons (in horizontalem Layout zentriert)---
    button_layout = QHBoxLayout() # Horizontales Layout für Buttons
    button_layout.addStretch(1) # Dehnbarer Raum links

    login_button = QPushButton("Login")
    login_button.setObjectName("LoginButton") # Für Styling
    login_button.setCursor(Qt.CursorShape.PointingHandCursor)
    login_button.clicked.connect(login_callback) # Signal verbinden
    button_layout.addWidget(login_button)

    button_layout.addSpacing(10) # Abstand zwischen Buttons

    register_button = QPushButton("Registrieren")
    register_button.setObjectName("RegisterButton") # Für Styling
    register_button.setCursor(Qt.CursorShape.PointingHandCursor)
    register_button.clicked.connect(register_callback) # Signal verbinden
    button_layout.addWidget(register_button)

    button_layout.addStretch(1) # Dehnbarer Raum rechts

    # Füge Button-Layout zum Hauptlayout hinzu
    main_layout.addLayout(button_layout)
    main_layout.addStretch(1) # Dehnt den Raum unter den Buttons

    # Setze das Layout für das Hauptwidget
    # main_widget.setLayout(main_layout) # Wird durch Übergabe im Konstruktor gesetzt

    # Gib Dictionary mit Referenzen zurück
    widgets = {
        "main_widget": main_widget,
        "username_entry": username_entry,
        "password_entry": password_entry,
        "login_button": login_button,
        "register_button": register_button,
        "welcome_label": welcome_label # Für evtl. Styling
    }
    return widgets

def create_chat_widget(back_callback, send_callback):
    """Erstellt das Chat-Widget (QWidget) mit PyQt6."""
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(10, 5, 10, 10) # Kleinere Ränder
    main_layout.setSpacing(5) # Kleinerer Abstand

    # --- Top Bar ---
    top_bar_widget = QWidget()
    top_bar_layout = QHBoxLayout(top_bar_widget)
    top_bar_layout.setContentsMargins(0, 0, 0, 0) # Kein Rand in der Leiste

    exit_button = QPushButton("Zurück")
    exit_button.setObjectName("BackButton")
    exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
    exit_button.clicked.connect(back_callback)
    top_bar_layout.addWidget(exit_button, 0) # Nimmt min. Platz (links)

    top_logo_label = QLabel() # Leeres Label als Platzhalter
    top_logo_pixmap: QPixmap | None = gui_utils.load_image(config.LOGO_PATH, config.TOP_BAR_LOGO_SIZE)
    if top_logo_pixmap:
        top_logo_label.setPixmap(top_logo_pixmap)
        top_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Minimum Größe, damit es nicht verschwindet
        top_logo_label.setMinimumSize(config.TOP_BAR_LOGO_SIZE[0], config.TOP_BAR_LOGO_SIZE[1])
    else:
        top_logo_label.setText("") # Kein Bild, kein Text

    top_bar_layout.addStretch(1) # Dehnbarer Raum links vom Logo
    top_bar_layout.addWidget(top_logo_label, 0, Qt.AlignmentFlag.AlignCenter) # Zentriert
    top_bar_layout.addStretch(1) # Dehnbarer Raum rechts vom Logo

    # top_bar_widget.setLayout(top_bar_layout) # Wird im Konstruktor gesetzt
    main_layout.addWidget(top_bar_widget) # Füge Leiste zum Hauptlayout hinzu

    # --- Chat Display ---
    chat_window = QTextEdit()
    chat_window.setObjectName("ChatWindow") # Für Styling
    chat_window.setReadOnly(True)
    # Scrollbars sind automatisch vorhanden
    # Styling (z.B. Padding) wird über Stylesheet in main_app gesetzt
    main_layout.addWidget(chat_window, 1) # Nimmt allen verfügbaren vertikalen Platz (Stretch Factor 1)

    # --- Input Area ---
    input_widget = QWidget()
    input_layout = QHBoxLayout(input_widget)
    input_layout.setContentsMargins(0, 0, 0, 0)
    input_layout.setSpacing(5)

    entry = QLineEdit()
    entry.setPlaceholderText("Nachricht eingeben...")
    input_layout.addWidget(entry, 1) # Nimmt verfügbaren horizontalen Platz

    send_button = QPushButton("Senden")
    send_button.setObjectName("SendButton")
    send_button.setCursor(Qt.CursorShape.PointingHandCursor)
    send_button.clicked.connect(send_callback)
    input_layout.addWidget(send_button, 0) # Nimmt min. Platz

    # input_widget.setLayout(input_layout) # Wird im Konstruktor gesetzt
    main_layout.addWidget(input_widget) # Füge Eingabebereich unten hinzu

    # Gib Dictionary mit Referenzen zurück
    widgets = {
        "main_widget": main_widget,
        "chat_window": chat_window,
        "entry": entry,
        "send_button": send_button,
        "exit_button": exit_button # Referenz auf den Zurück-Button
    }
    return widgets