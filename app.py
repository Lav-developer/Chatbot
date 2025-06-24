import google.generativeai as ai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("Error: API_KEY not found in .env file.")
    exit(1)

ai.configure(api_key=API_KEY)

model = ai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

print("Chatbot: Hello! Type 'Bye' or 'Exit' to exit and 'clear' to reset the chat.")

with open("chat_log.txt", "a", encoding="utf-8") as log_file:
    while True:
        message = input('You: ')
        if message.lower() in ['bye', 'exit']:
            print('Chatbot: Bye Bye, Have a great day!')
            log_file.write("You: bye/exit\nChatbot: Bye Bye, Have a great day!\n")
            break
        if message.lower() == 'clear':
            chat = model.start_chat()
            print("Chatbot: Chat history cleared.")
            log_file.write("You: clear\nChatbot: Chat history cleared.\n")
            continue
        if message.lower() == 'history':
            print("Chatbot: Showing chat history...\n")
            try:
                with open("chat_log.txt", "r", encoding="utf-8") as history_file:
                    history = history_file.read()
                    print(history if history else "No chat history found.")
            except Exception as e:
                print(f"Chatbot: Could not read chat history. Error: {e}")
            continue
        try:
            response = chat.send_message(message)
            print('Chatbot:', response.text)
            log_file.write(f"You: {message}\nChatbot: {response.text}\n")
        except Exception as e:
            print("Chatbot: Sorry, something went wrong.")
            log_file.write(f"You: {message}\nChatbot: Error: {e}\n")