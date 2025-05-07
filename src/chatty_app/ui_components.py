# src/chatty_app/ui_components.py
import tkinter as tk
from tkinter import ttk
from . import config
from . import gui_utils

# --- KORRIGIERTE Funktion ---
def create_start_frame(parent, login_callback, register_callback): # <-- Akzeptiert jetzt zwei Callbacks
    """Erstellt den Frame für die Startseite mit Login/Register."""
    start_frame = ttk.Frame(parent, padding="20", style="TFrame")

    # Logo
    logo_image_tk = gui_utils.load_image(config.LOGO_PATH, config.LOGO_SIZE)
    logo_label = None
    if logo_image_tk:
        logo_label = ttk.Label(start_frame, image=logo_image_tk, background=config.BG_COLOR)
        logo_label.image = logo_image_tk # Referenz behalten!
        logo_label.pack(pady=(20, 15))

    # Willkommenstext
    welcome_label = ttk.Label(start_frame, text="Willkommen bei Chatty!", font=(config.FONT_FAMILY, config.FONT_SIZE_XLARGE, "bold"), background=config.BG_COLOR, foreground=config.FG_COLOR)
    welcome_label.pack(pady=(0 if logo_label else 50, 10))

    # Benutzername Eingabe
    username_label = ttk.Label(start_frame, text="Benutzername:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), background=config.BG_COLOR, foreground=config.FG_COLOR)
    username_label.pack(pady=(10, 2), anchor='w', padx=50)
    username_entry = ttk.Entry(start_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE), style="TEntry", width=30)
    username_entry.pack(pady=(0, 10), padx=50, fill='x')

    # Passwort Eingabe
    password_label = ttk.Label(start_frame, text="Passwort:", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), background=config.BG_COLOR, foreground=config.FG_COLOR)
    password_label.pack(pady=(5, 2), anchor='w', padx=50)
    password_entry = ttk.Entry(start_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE), style="TEntry", width=30, show="*") # Zeige Sternchen
    password_entry.pack(pady=(0, 20), padx=50, fill='x')

    # Button Frame für Login/Register nebeneinander
    button_frame = ttk.Frame(start_frame, style="TFrame")
    button_frame.pack(pady=10)

    # Login Button - verwendet login_callback
    login_button = ttk.Button(button_frame, text="Login", command=login_callback, style="Start.TButton", cursor="hand2")
    login_button.pack(side=tk.LEFT, padx=10)

    # Register Button - verwendet register_callback
    register_button = ttk.Button(button_frame, text="Registrieren", command=register_callback, style="Start.TButton", cursor="hand2")
    register_button.pack(side=tk.LEFT, padx=10)

    # Gib Frame und wichtige Eingabefelder zurück
    widgets = {
        "start_frame": start_frame,
        "username_entry": username_entry,
        "password_entry": password_entry,
        "login_button": login_button,
        "register_button": register_button
    }
    return widgets # <-- Gib das Dictionary zurück

# --- create_chat_frame bleibt unverändert ---
def create_chat_frame(parent, back_callback, send_callback):
    chat_main_frame = ttk.Frame(parent, style="TFrame")

    top_bar_frame = ttk.Frame(chat_main_frame, style="TFrame")
    top_bar_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
    exit_button = ttk.Button(top_bar_frame, text="Zurück", command=back_callback, style="Exit.TButton", cursor="hand2")
    exit_button.grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')
    top_logo_image_tk = gui_utils.load_image(config.LOGO_PATH, config.TOP_BAR_LOGO_SIZE)
    if top_logo_image_tk:
        top_logo_label = ttk.Label(top_bar_frame, image=top_logo_image_tk, background=config.BG_COLOR)
        top_logo_label.image = top_logo_image_tk
        top_logo_label.grid(row=0, column=1, pady=1, padx=(0, 85))
    top_bar_frame.columnconfigure(0, weight=0)
    top_bar_frame.columnconfigure(1, weight=1)
    top_bar_frame.columnconfigure(2, weight=0)

    chat_display_frame = ttk.Frame(chat_main_frame, padding="0", style="TFrame")
    chat_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 0))
    scrollbar = ttk.Scrollbar(chat_display_frame, orient=tk.VERTICAL, style="Vertical.TScrollbar")
    chat_window = tk.Text(
        chat_display_frame, wrap=tk.WORD, state='disabled', bg=config.TEXT_AREA_BG, fg=config.FG_COLOR,
        font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL), padx=10, pady=10, yscrollcommand=scrollbar.set,
        relief="flat", borderwidth=0, highlightthickness=0
    )
    scrollbar.config(command=chat_window.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    chat_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    gui_utils.configure_tags(chat_window)

    input_frame = ttk.Frame(chat_main_frame, padding="10 10 10 10", style="TFrame")
    input_frame.pack(fill=tk.X, padx=10, pady=10)
    entry = ttk.Entry(input_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE), style="TEntry")
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
    send_button = ttk.Button(input_frame, text="Senden", command=send_callback, style="TButton")
    send_button.pack(side=tk.LEFT, padx=(10, 0))
    entry.bind("<Return>", lambda event: send_callback())

    widgets = {
        "main_frame": chat_main_frame,
        "chat_window": chat_window,
        "entry": entry,
        "send_button": send_button,
        "exit_button": exit_button
    }
    return widgets