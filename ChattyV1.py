import tkinter as tk

# --- Chatbot Logik ---
def chatty_response(user_input):
    user_input = user_input.lower()

    if "hallo" in user_input or "hi" in user_input:
        return "Hey! Wie kann ich dir helfen?"
    elif "wie geht's" in user_input or "wie geht es dir" in user_input:
        return "Mir geht's gut, danke! Und dir?"
    elif "hilfe" in user_input:
        return "Natürlich! Ich bin hier, um dir zu helfen. Was brauchst du?"
    elif "tschüss" in user_input or "bye" in user_input:
        return "Tschüss! Schön, mit dir gequatscht zu haben. :)"
    else:
        return "Das habe ich leider nicht verstanden."

# --- GUI ---
def send_message():
    user_input = entry.get()
    if user_input.strip() == "":
        return

    chat_window.config(state='normal')
    chat_window.insert(tk.END, "Du: " + user_input + "\n")
    response = chatty_response(user_input)
    chat_window.insert(tk.END, "Chatty: " + response + "\n\n")
    chat_window.config(state='disabled')
    
    entry.delete(0, tk.END)

# Fenster einrichten
root = tk.Tk()
root.title("Chatty - Dein kleiner Chatbot")
root.geometry("400x500")

# Chat-Fenster (Textbereich)
chat_window = tk.Text(root, state='disabled', wrap='word', bg="#F0F0F0", font=("Arial", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Eingabezeile
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=(0,10), fill=tk.X)
entry.bind("<Return>", lambda event: send_message())

# Senden-Button
send_button = tk.Button(root, text="Senden", command=send_message)
send_button.pack(padx=10, pady=(0, 10))

# Hauptloop starten
root.mainloop()
