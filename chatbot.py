
import difflib
import random
from datetime import datetime

class ChatBot:
    def __init__(self):
        self.responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! Ready to chat.",
            "how are you": "I'm just a bot, but I'm functioning perfectly! How about you?",
            "name": "I am a Python Chatbot v2.0.",
            "time": lambda: f"The current time is {datetime.now().strftime('%H:%M')}.",
            "joke": self.get_random_joke,
            "bye": "Goodbye! Have a great day!",
            "help": "I can tell you the time, a joke, or just chat. Try saying 'hello'!"
        }
        self.jokes = [
            "Why do Python programmers prefer dark mode? Because light attracts bugs!",
            "Why did the developer go broke? Because he used up all his cache.",
            "What do you call a snake that analyzes data? A Py-thon!"
        ]

    def get_random_joke(self):
        return random.choice(self.jokes)

    def get_response(self, user_input):
        user_input = user_input.lower().strip()
        
        # 1. Exact match
        if user_input in self.responses:
            response = self.responses[user_input]
            return response() if callable(response) else response

        # 2. Fuzzy match (find similar words)
        matches = difflib.get_close_matches(user_input, self.responses.keys(), n=1, cutoff=0.6)
        if matches:
            matched_key = matches[0]
            response = self.responses[matched_key]
            reply = response() if callable(response) else response
            return f"Did you mean '{matched_key}'? {reply}"

        return "I'm not sure I understand. Type 'help' to see what I can do."

    def start(self):
        print("🤖 Chatbot: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if not user_input:
                continue
            
            if user_input.lower() == "bye":
                print(f"🤖 Chatbot: {self.responses['bye']}")
                break
                
            response = self.get_response(user_input)
            print(f"🤖 Chatbot: {response}")

if __name__ == "__main__":
    bot = ChatBot()
    bot.start()
