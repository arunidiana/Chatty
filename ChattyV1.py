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
        return "Das habe ich leider nicht verstanden. Magst du das anders formulieren?"

def start_chat():
    print("👋 Hallo, ich bin Chatty – dein kleiner Chatbot! (Tippe 'bye' zum Beenden)")
    while True:
        user_input = input("Du: ")
        if user_input.lower() in ["bye", "tschüss", "auf wiedersehen"]:
            print("Chatty: Tschüss! Bis zum nächsten Mal! 👋")
            break
        response = chatty_response(user_input)
        print(f"Chatty: {response}")

if __name__ == "__main__":
    start_chat()
