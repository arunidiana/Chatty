# src/chatty_app/ui_components_qt.py
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QScrollArea, QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from . import config
from . import gui_utils

def create_start_widget(login_callback, register_callback):
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(10)

    logo_pixmap = gui_utils.load_image(config.LOGO_PATH, config.LOGO_SIZE)
    if logo_pixmap:
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setMinimumSize(config.LOGO_SIZE[0], config.LOGO_SIZE[1])
        main_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(15)

    welcome_label = QLabel("Willkommen bei Chatty!")
    welcome_label.setObjectName("WelcomeLabel")
    welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(welcome_label)
    main_layout.addSpacing(10)

    username_label = QLabel("Benutzername:")
    username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    main_layout.addWidget(username_label)

    username_entry = QLineEdit()
    username_entry.setPlaceholderText("Benutzernamen eingeben")
    username_entry.setObjectName("UsernameEntry")
    main_layout.addWidget(username_entry)
    main_layout.addSpacing(10)

    password_label = QLabel("Passwort:")
    password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    main_layout.addWidget(password_label)

    password_entry = QLineEdit()
    password_entry.setPlaceholderText("Passwort eingeben")
    password_entry.setEchoMode(QLineEdit.EchoMode.Password)
    password_entry.setObjectName("PasswordEntry")
    main_layout.addWidget(password_entry)
    main_layout.addSpacing(20)

    button_layout = QHBoxLayout()
    button_layout.addStretch(1)

    login_button = QPushButton("Login")
    login_button.setObjectName("LoginButton")
    login_button.setCursor(Qt.CursorShape.PointingHandCursor)
    login_button.clicked.connect(login_callback)
    button_layout.addWidget(login_button)

    button_layout.addSpacing(10)

    register_button = QPushButton("Registrieren")
    register_button.setObjectName("RegisterButton")
    register_button.setCursor(Qt.CursorShape.PointingHandCursor)
    register_button.clicked.connect(register_callback)
    button_layout.addWidget(register_button)

    button_layout.addStretch(1)

    main_layout.addLayout(button_layout)
    main_layout.addStretch(1)

    widgets = {
        "main_widget": main_widget,
        "username_entry": username_entry,
        "password_entry": password_entry,
        "login_button": login_button,
        "register_button": register_button,
        "welcome_label": welcome_label
    }
    return widgets

def create_chat_widget(back_callback, send_callback):
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(10, 5, 10, 10)
    main_layout.setSpacing(5)

    top_bar_widget = QWidget()
    top_bar_layout = QHBoxLayout(top_bar_widget)
    top_bar_layout.setContentsMargins(0, 0, 0, 0)

    exit_button = QPushButton("Zurück")
    exit_button.setObjectName("BackButton")
    exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
    exit_button.clicked.connect(back_callback)
    top_bar_layout.addWidget(exit_button, 0)

    top_logo_label = QLabel()
    top_logo_pixmap: QPixmap | None = gui_utils.load_image(config.LOGO_PATH, config.TOP_BAR_LOGO_SIZE)
    if top_logo_pixmap:
        top_logo_label.setPixmap(top_logo_pixmap)
        top_logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_logo_label.setMinimumSize(config.TOP_BAR_LOGO_SIZE[0], config.TOP_BAR_LOGO_SIZE[1])
    else:
        top_logo_label.setText("")
    top_logo_label.setObjectName("TopBarLogo")

    top_bar_layout.addStretch(1)
    top_bar_layout.addWidget(top_logo_label, 0, Qt.AlignmentFlag.AlignCenter)
    top_bar_layout.addStretch(1)

    main_layout.addWidget(top_bar_widget)

    chat_window = QTextEdit()
    chat_window.setObjectName("ChatWindow")
    chat_window.setReadOnly(True)
    main_layout.addWidget(chat_window, 1)

    input_widget = QWidget()
    input_layout = QHBoxLayout(input_widget)
    input_layout.setContentsMargins(0, 0, 0, 0)
    input_layout.setSpacing(5)

    entry = QLineEdit()
    entry.setPlaceholderText("Nachricht eingeben...")
    entry.setObjectName("ChatEntry")
    input_layout.addWidget(entry, 1)

    send_button = QPushButton("Senden")
    send_button.setObjectName("SendButton")
    send_button.setCursor(Qt.CursorShape.PointingHandCursor)
    send_button.clicked.connect(send_callback)
    input_layout.addWidget(send_button, 0)

    main_layout.addWidget(input_widget)

    widgets = {
        "main_widget": main_widget,
        "chat_window": chat_window,
        "entry": entry,
        "send_button": send_button,
        "exit_button": exit_button
    }
    return widgets