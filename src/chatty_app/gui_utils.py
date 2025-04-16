# src/chatty_app/gui_utils.py
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import config # Importiere config für Farben und Pfade

def load_image(path, size):
    """Lädt ein Bild, skaliert es und gibt ein Tkinter-kompatibles Objekt zurück."""
    try:
        if os.path.exists(path):
            img_pil = Image.open(path)
            img_pil.thumbnail(size, Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil)
            return img_tk
        else:
            print(f"Warnung: Bilddatei nicht gefunden unter {path}")
            return None
    except ImportError:
        print("Fehler: Pillow fehlt. 'pip install Pillow'.")
        return None
    except Exception as e:
        print(f"Fehler beim Laden des Bildes {path}: {e}")
        return None

def insert_bubble(text_widget, text, tag_name, is_first_message=False):
    """Fügt eine formatierte Textblase (mit optionaler Trennlinie) in das Text-Widget ein."""
    text_widget.config(state='normal')
    if not is_first_message:
        separator_text = "─" * config.SEPARATOR_LENGTH
        text_widget.insert(tk.END, f"\n{separator_text}\n\n", "separator_line")
    text_widget.insert(tk.END, text + "\n", tag_name)
    text_widget.config(state='disabled')
    text_widget.see(tk.END)

def configure_tags(text_widget):
    """Konfiguriert die Tags für Textblasen und Trennlinien."""
    text_widget.tag_configure("user_bubble", background=config.BUBBLE_COLOR, foreground=config.BUBBLE_FG, justify=tk.RIGHT, lmargin1=80, lmargin2=80, rmargin=10, wrap=tk.WORD, borderwidth=0, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL))
    text_widget.tag_configure("bot_bubble", background=config.BUBBLE_COLOR, foreground=config.BUBBLE_FG, justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=80, wrap=tk.WORD, borderwidth=0, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL))
    text_widget.tag_configure("error_bubble", background=config.ERROR_BUBBLE_BG, foreground=config.ERROR_BUBBLE_FG, justify=tk.LEFT, lmargin1=10, lmargin2=10, rmargin=80, wrap=tk.WORD, borderwidth=0, font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, "italic"))
    text_widget.tag_configure("separator_line", foreground=config.SEPARATOR_COLOR, justify=tk.CENTER, font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL))

def configure_styles():
    """Konfiguriert die ttk-Styles für die Anwendung."""
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        print("Theme 'clam' nicht verfügbar, verwende Standard-Theme.")

    style.configure("TButton", font=(config.FONT_FAMILY, config.FONT_SIZE_NORMAL, "bold"), padding=8, foreground=config.ENTRY_BG_COLOR, background=config.ACCENT_COLOR, borderwidth=0, relief="flat")
    style.map("TButton", background=[('active', '#0056b3')])
    style.configure("Exit.TButton", font=(config.FONT_FAMILY, config.FONT_SIZE_SMALL), padding=5, foreground=config.ENTRY_BG_COLOR, background=config.EXIT_COLOR, borderwidth=0, relief="flat")
    style.map("Exit.TButton", background=[('active', '#808080')])
    style.configure("Start.TButton", font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE, "bold"), padding=15)
    style.map("Start.TButton", background=[('active', '#0056b3')])
    style.configure("TEntry", font=(config.FONT_FAMILY, config.FONT_SIZE_LARGE), padding=10, foreground=config.FG_COLOR, fieldbackground=config.ENTRY_BG_COLOR, borderwidth=1, relief="solid")
    style.configure("TFrame", background=config.BG_COLOR)
    style.configure("Vertical.TScrollbar", troughcolor=config.BG_COLOR, background=config.ACCENT_COLOR, borderwidth=0, arrowsize=0)
    style.map("Vertical.TScrollbar", background=[('active', '#0056b3')])
    return style