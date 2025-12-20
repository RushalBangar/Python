def smart_chatbot():
    print("🤖 Bot: I am listening for keywords! (Type 'bye' to exit)")

    # Dictionary: Keyword -> Response
    # We map a specific "trigger word" to a response
    responses = {
        "joke": "Why do Java programmers wear glasses? Because they don't C#!",
        "python": "Python is great for AI because of libraries like Pandas and NumPy.",
        "ai": "Artificial Intelligence is about making machines think and learn.",
        "name": "I am SmartBot v4.0.",
        "hello": "Hi there! How can I help?",
        "help": "I can tell you about AI, Python, or tell a joke!"
    }

    while True:
        user_input = input("\nYou: ").lower()

        if "bye" in user_input:
            print("🤖 Bot: Goodbye!")
            break

        # This variable tracks if we found an answer
        found_match = False

        # Loop through every keyword in our dictionary
        for keyword in responses:
            # CHECK: Is the keyword inside the user's input?
            if keyword in user_input:
                print(f"🤖 Bot: {responses[keyword]}")
                found_match = True
                break # Stop searching once we find a match!

        # If the loop finishes and found_match is still False
        if not found_match:
            print("🤖 Bot: I'm not sure what that means. Try asking about 'AI' or 'Python'.")

smart_chatbot()