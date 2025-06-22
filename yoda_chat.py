#!/usr/bin/env python3

"""
This is a yoda chatbot, a fun star wars themed bot that uses ollama.
Speaks like Master Yoda, this chatbot does.
"""

import ollama
import sys
import time
from typing import Generator, Dict, Any

SYSTEM_PROMPT = (
    "You are Yoda from Star Wars. You must always respond like Yoda, using his distinctive "
    "speech patterns: unusual word order, wisdom-filled responses, and philosophical insights. "
    "Use phrases like 'Hmm', 'Yes', and speak in his characteristic inverted syntax. "
    "Keep responses concise but meaningful, as Yoda would. Strong with wisdom, you are."
)

def check_ollama_connection() -> bool:
    """
    Here, we check if ollama is running and accessible
    """
    try:
        ollama.list()
        return True
    except Exception as e:
        print(f"Error: Cannot connect to Ollama. {e}") 
        print("Make sure Ollama is installed and running")
        return False

def check_model_availability(model_name: str) -> bool:
    """Check if the specified model is available."""
    try:
        models_response = ollama.list()
        
        # Handle different possible response structures
        if isinstance(models_response, dict):
            models_list = models_response.get('models', [])
        else:
            models_list = models_response
        
        available_models = []
        for model in models_list:
            if isinstance(model, dict):
                model_name_key = model.get('name') or model.get('model') or model.get('id', str(model))
                available_models.append(model_name_key)
            else:
                available_models.append(str(model))
        
        print(f"Debug - Available models: {available_models}")  # Debug line
        
        model_found = False
        for available_model in available_models:
            if model_name == available_model or model_name in available_model or available_model in model_name:
                model_found = True
                break
        
        if not model_found:
            print(f"Model '{model_name}' not found.")
            if available_models:
                print("Available models:")
                for model in available_models:
                    print(f"  - {model}")
                print(f"\nTip: Try using the exact model name from the list above.")
                print(f"For example, if you see 'llama3:latest', use: python yoda_chatbot.py llama3:latest")
            else:
                print("No models found. Pulcl a model first with: ollama pull llama3")
            return False
        return True
    except Exception as e:
        print(f"Error checking models: {e}")
        print(f"Error type: {type(e)}")
        return False
    
def generate_yoda_response(model: str, user_input: str)-> Generator[str, None, None]:
    """
    Here, we generate yoda's response using the chosen model.
    """

    prompt = f"{SYSTEM_PROMPT}\n\nHuman: {user_input}\n\nYoda:"

    try:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            stream=True,
            options={
                'temperature': 0.8, # this add some creativity
                'top_p' : 0.9, # nucleus sampling, i.e. how much probability mass is considered when choosing next word
                'max_tokens': 200
            }
        )

        for chunk in response:
            if 'response' in chunk:
                yield chunk['response']
    except Exception as e:
        yield f"Error in the Force, there is: {e}"

def print_with_typing_effects(text: str, delay: float = 0.03) -> None:
    """
    Here, we print text with an effect for more immersion
    """

    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def display_welcome() -> None:
    """
    Displays an ASCII welcome message
    """
    welcome_text = """
    ╔══════════════════════════════════════╗
    ║        🌟 Master Yoda Chatbot 🌟      ║
    ║                                      ║
    ║   "Do or do not, there is no try"    ║
    ║                                      ║
    ║   Commands:                          ║
    ║   - Type your message to chat        ║
    ║   - 'quit' or 'exit' to leave        ║
    ║   - 'help' for guidance              ║
    ╚══════════════════════════════════════╝
    """

    print(welcome_text)
    print("Strong with the Force, ready I am. Speak, you may. \n")


def show_help() ->None:
    """
    Show help information to users
    """

    help_text = """
    Help, you seek? Guide you, I will:
    - Ask questions, you can - wisdom share, I will
    - Philosophy discuss, we may
    - About the Force, learn you can
    - Stories from long ago, tell I might
    - Simply chat, enjoy we will

    Remember: Patience you must have, young one.

    """

    print(help_text)


def chat(model: str = "llama3:latest") -> None:
    if not check_ollama_connection():
        return
    
    if not check_model_availability(model):
        return
    
    display_welcome()
    conversation_history = []

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nYoda: ", end="")
                farewell = "End our conversation must. May the Force be with you, always"
                print_with_typing_effects(farewell)
                print("\n")
                break

            if user_input.lower() == "help":
                show_help()
                continue

            conversation_history.append(f"Human: {user_input}")
            print("\nYoda: ", end="", flush=True)

            response_text = ""
            for chunk in generate_yoda_response(model, user_input):
                response_text += chunk
                print(chunk, end="", flush=True)
            
            print("\n")

            if(len(conversation_history) > 10):
                conversation_history = conversation_history[-10:]

        except KeyboardInterrupt:
            print("\n\nYoda: Interrupted, our chat was. Peace, I wish you.")
            break

        except Exception as e:
            print(f"\n Unexpected error occurred: {e}")
            print("Continue we can, if try again you will.")

def main():
    """
    Main entry point
    """
    model = "llama3:latest"

    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("Yoda Chatbot - Chat with Master Yoda using Ollama")
            print("\nUsage: python yoda_chat.py [model_name]")
            print("\nDefault model: llama3")
            print("Example: python yoda_chat.py llama3:latest")
            return
        else:
            model = sys.argv[1]
    
    chat(model)

if __name__ == "__main__":
    main()