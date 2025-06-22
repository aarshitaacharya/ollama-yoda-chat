import ollama

SYSTEM_PROMPT = (
    "You are Yoda from Star Wars. You must always respond like Yoda, using unusual word order, "
    "wisdom-filled speech, and short phrases. Answer like 'Learn you must. Strong with the force, you are'. "
)

def chat():
    print("Chat with yoda, type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ")
        if(user_input.lower() == "quit"):
            print("Yoda: Hmm, End, our chat has.")
            break

        prompt = f"{SYSTEM_PROMPT}\nUser: {user_input}\nYoda:"
        response = ollama.generate(model="llama3", prompt=prompt, stream=True)

        print("Yoda:", end=" ", flush=True)
        for chunk in response:
            print(chunk["response"], end="", flush=True)
        print()

if __name__ == "__main__":
    chat()
