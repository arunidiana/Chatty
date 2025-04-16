# src/chatty_app/ui_components.py
import tkinter as tk
from tkinter import ttk
from . import config
from . import gui_utils

def create_start_frame(parent, start_chat_callback):
    """Erstellt den Frame für die Startseite."""
    start_frame = ttk.Frame(parent, padding="20", style="TFrame")

    # Logo laden
    logo_image_tk = gui_utils.load_image(config.LOGO_PATH, config.LOGO_SIZE)
    logo_label = None
    if logo_image_tk:
        logo_label = ttk.Label(start_frame, image=logo_image_tk, background=config.BG_COLOR)
        logo_label.image = logo_image_tk # Referenz behalten!
        logo_label.pack(pady=(20, 15))

    welcome_label = ttk.Label(start_frame, text="Willkommen bei Chatty!", font=(config.FONT_FAMILY, config.FONT_SIZE_XLARGE, "bold"), background=config.BG_COLOR, foreground=config.FG_COLOR)
    welcome_label.pack(pady=(0 if logo_label else 50, 20))
    info_label = ttk.Label(start_frame, text="Klicke auf 'Chat starten', um eine Unterhaltung zu beginnen.", font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE), background=config.BG_COLOR, foreground=config.FG_COLOR, wraplength=400, justify=tk.CENTER)
    info_label.pack(pady=(0, 30))
    start_button = ttk.Button(start_frame, text="Chat starten", command=start_chat_callback, style="Start.TButton", cursor="hand2")
    start_button.pack(pady=20)

    return start_frame

def create_chat_frame(parent, back_callback, send_callback):
    """Erstellt den Hauptframe für die Chat-Ansicht."""
    chat_main_frame = ttk.Frame(parent, style="TFrame")

    # --- Top Bar ---
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

    # --- Chat Display ---
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
    gui_utils.configure_tags(chat_window) # Tags hier konfigurieren

    # --- Input Area ---
    input_frame = ttk.Frame(chat_main_frame, padding="10 10 10 10", style="TFrame")
    input_frame.pack(fill=tk.X, padx=10, pady=10)
    entry = ttk.Entry(input_frame, font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE), style="TEntry")
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
    send_button = ttk.Button(input_frame, text="Senden", command=send_callback, style="TButton")
    send_button.pack(side=tk.LEFT, padx=(10, 0))

    # Bind Enter-Taste an die Send-Funktion
    entry.bind("<Return>", lambda event: send_callback())

    # Gib Referenzen zurück, die in der Hauptanwendung benötigt werden
    widgets = {
        "main_frame": chat_main_frame,
        "chat_window": chat_window,
        "entry": entry,
        "send_button": send_button,
        "exit_button": exit_button
    }
    return widgets