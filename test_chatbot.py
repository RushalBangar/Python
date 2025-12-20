import unittest
from chatbot import ChatBot

class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.bot = ChatBot()

    def test_exact_match(self):
        self.assertEqual(self.bot.get_response("hello"), "Hello! How can I help you today?")
        self.assertEqual(self.bot.get_response("name"), "I am a Python Chatbot v2.0.")

    def test_fuzzy_match(self):
        # "helo" -> "hello"
        response = self.bot.get_response("helo")
        self.assertTrue("Did you mean 'hello'?" in response)
        
        # "tme" -> "time"
        response = self.bot.get_response("tme")
        self.assertTrue("Did you mean 'time'?" in response)

    def test_unknown_input(self):
        response = self.bot.get_response("xyz123")
        self.assertEqual(response, "I'm not sure I understand. Type 'help' to see what I can do.")

if __name__ == '__main__':
    unittest.main()
