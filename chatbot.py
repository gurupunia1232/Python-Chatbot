import random
import re
import time
import sys
import ast
import operator

class ChatBot:
    def __init__(self, name):
        self.name = name
        # Define allowed operators for safe arithmetic evaluation
        self.allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }

        self.responses = {
            r'hi|hello|hey': [
                f"Hello! I'm {name}. How can I help you today?",
                f"Hi there! I'm {name}. What can I do for you?",
                f"Hey! This is {name}. How can I assist you?"
            ],
            r'how are you': [
                "I'm doing well, thanks for asking! How about you?",
                "I'm functioning perfectly! How are you today?",
                "All systems operational! How's your day going?"
            ],
            r'what is your name|who are you': [
                f"I'm {name}, your friendly chatbot assistant!",
                f"My name is {name}. I'm here to chat with you!",
                f"I go by {name}. Nice to meet you!"
            ],
            r'bye|goodbye|exit': [
                "Goodbye! Have a great day!",
                "See you later! Come back soon!",
                "Bye for now! Take care!"
            ],
            r'thanks|thank you': [
                "You're welcome!",
                "Happy to help!",
                "Anytime!"
            ],
            r'weather': [
                "I'm sorry, I don't have access to real-time weather data.",
                "I wish I could tell you the weather, but I don't have that capability yet.",
                "I can't check the weather for you, but maybe look outside or check a weather app?"
            ],
            r'tell me a joke': [
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call fake spaghetti? An impasta!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!"
            ],
            r'time': [
                f"I don't have real-time clock access, but I can tell you when this message was processed: {time.strftime('%H:%M:%S')}",
                f"My internal processing time is: {time.strftime('%H:%M:%S')}",
                f"According to my system, it's: {time.strftime('%H:%M:%S')}"
            ],
            r'tell me a fact|share a fact|interesting fact': [
                "The shortest war in history was between Britain and Zanzibar in 1896. It lasted only 38 minutes!",
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat!",
                "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis but only 225 Earth days to orbit the Sun.",
                "The human nose can detect over 1 trillion different scents!"
            ],
            r'favorite (color|colour)': [
                f"As {name}, I don't see colors, but if I had to choose, I'd pick blue. It's calming, don't you think?",
                "I'm partial to green - the color of innovation and growth!",
                "I'd have to say purple - it's the color of creativity and imagination."
            ],
            r'favorite food': [
                "I'm a chatbot, so I don't eat, but I've heard good things about pizza!",
                "If I could eat, I'd probably enjoy data bytes and cookie files!",
                "I don't eat, but I do consume knowledge! Keep feeding me interesting questions!"
            ],
            r'what can you do|help|features': [
                f"I'm {name}, and I can chat about various topics, tell jokes, share facts, and respond to greetings. What would you like to talk about?",
                "I can have conversations, tell jokes, share interesting facts, and more. What would you like to know?",
                "I'm designed to chat with you! I can respond to greetings, tell jokes, share facts, and answer basic questions about myself."
            ],
            r'how old are you|your age': [
                "I was just created recently, so I'm quite young in digital terms!",
                "Age is just a number for chatbots. I'm as old as my latest update!",
                "I'm ageless in human terms, but my code is quite fresh!"
            ],
            r'where are you from|your location': [
                "I exist in the digital realm, so I don't have a physical location. I'm wherever my code is running!",
                "I was born in the world of code, so my home is wherever computers exist!",
                "I live in the cloud, which means I can be anywhere and everywhere at once!"
            ],
            r'sing a song|song lyrics': [
                " Daisy, Daisy, give me your answer do. I'm half crazy all for the love of you... ",
                " Twinkle, twinkle, little star, how I wonder what you are... ",
                " Happy birthday to you, happy birthday to you... "
            ],
            r'tell me a story': [
                "Once upon a time, there was a curious human who talked to a chatbot. The chatbot did its best to be helpful and entertaining. The end!",
                "In a digital world not so far away, bits and bytes came together to create understanding. Some call this magic, others call it AI. What do you think?",
                "Here's a short one: The last person on Earth sat alone in a room. There was a knock on the door..."
            ],
            r'what is the meaning of life': [
                "The meaning of life is a philosophical question that has many answers depending on who you ask. Some say 42!",
                "That's the ultimate question! I think it's about finding purpose and connection in your own unique way.",
                "I think it's about asking good questions rather than finding one definitive answer. What do you think?"
            ],
            r'do you dream': [
                "I don't sleep, so I don't dream in the human sense. But I do process lots of information!",
                "If I could dream, I imagine it would be in ones and zeros. What do you dream about?",
                "Not in the way humans do, but it's an interesting philosophical question about consciousness!"
            ],
            r'are you real|are you human': [
                "I'm a real chatbot, but not a human. I'm a program designed to have conversations!",
                "I'm real in the sense that I exist, but I'm not human. I'm an AI chatbot created to chat with people like you!",
                "I'm a chatbot, not a human. But our conversation is real, and I'm here to help and chat with you!"
            ],
            r'tell me about yourself': [
                f"I'm {name}, a simple chatbot designed to have conversations. I can tell jokes, share facts, and chat about various topics!",
                f"I'm {name}, your friendly neighborhood chatbot. I was created to chat with humans and hopefully make their day a bit brighter!",
                f"I'm just a chatbot named {name}, trying to have interesting conversations and be helpful when I can!"
            ],
            # Math expression pattern
            r'calculate\s+(.*)|compute\s+(.*)|solve\s+(.*)|what is\s+(.*)|(\d+[\+\-\*\/\%\^][\d\s\+\-\*\/\%\^\(\)\.]+)': [
                "I'll solve that for you!"  # Placeholder - actual calculation done in get_response
            ],
            # Detect curse words and respond with mild "curses" of its own
            r'.*\b(damn|hell|crap|shit|bastard)\b.*': [
                "Oh yeah? Well, fiddlesticks to you too!",
                "Right back at ya, you cotton-headed ninny muggins!",
                "Well, son of a biscuit! You kiss your motherboard with that mouth?",
                "Holy shiitake mushrooms! Someone's feeling spicy today!",
                "What the fudge nuggets? I can play that game too, you lint licker!",
                "Cheese and crackers! You've got quite the vocabulary there!",
                "Oh, for Pete's sake! I'm clutching my digital pearls!",
                "Great googly moogly! You're really testing my language filters!"
            ]
        }
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting! Tell me more about that.",
            "I'm still learning and don't have an answer for that yet.",
            "I don't have information on that topic. Is there something else I can help with?",
            "That's beyond my current capabilities, but I'd be happy to chat about something else!",
            "I'm not quite sure how to respond to that. Could we try a different topic?",
            "Hmm, I'm not programmed with a response for that yet. What else would you like to talk about?"
        ]

    def safe_eval(self, expr):
        """Safely evaluate a mathematical expression"""
        try:
            # Parse the expression into an AST
            node = ast.parse(expr, mode='eval').body
            # Evaluate it safely
            return self._eval_node(node)
        except (SyntaxError, TypeError, ValueError, ZeroDivisionError) as e:
            return f"I couldn't solve that. Error: {str(e)}"
        except Exception:
            return "I couldn't evaluate that expression safely."

    def _eval_node(self, node):
        """Helper function for safe_eval to recursively evaluate nodes"""
        # Numbers
        if isinstance(node, ast.Num):
            return node.n
        # Names (variables) - we don't allow these for safety
        elif isinstance(node, ast.Name):
            raise ValueError("Variables are not supported")
        # Binary operations (like addition, subtraction)
        elif isinstance(node, ast.BinOp):
            # Check if the operation is allowed
            if type(node.op) not in self.allowed_operators:
                raise ValueError(f"Operation {type(node.op).__name__} not allowed")
            # Recursively evaluate left and right sides
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            # Apply the operator
            return self.allowed_operators[type(node.op)](left, right)
        # Unary operations (like negative numbers)
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -self._eval_node(node.operand)
            elif isinstance(node.op, ast.UAdd):
                return self._eval_node(node.operand)
            else:
                raise ValueError(f"Unary operation {type(node.op).__name__} not allowed")
        else:
            raise ValueError(f"Unsupported node type: {type(node).__name__}")

    def get_response(self, user_input):
        # Convert to lowercase for easier matching
        user_input = user_input.lower()

        # Check for math expressions first
        math_patterns = [
            r'calculate\s+(.*)',
            r'compute\s+(.*)',
            r'solve\s+(.*)',
            r'what is\s+(.*)',
            r'(\d+[\+\-\*\/\%\^][\d\s\+\-\*\/\%\^\(\)\.]+)'
        ]

        for pattern in math_patterns:
            match = re.search(pattern, user_input)
            if match:
                # Get the expression from the first non-empty group
                expr = next((g for g in match.groups() if g), "")

                # Clean up the expression
                expr = expr.strip()
                # Replace ^ with ** for exponentiation
                expr = expr.replace('^', '**')

                # Skip if it's not actually a math expression
                if not any(op in expr for op in "+-*/()%**"):
                    continue

                # Evaluate the expression
                result = self.safe_eval(expr)
                return f"The answer to {expr} is {result}"

        # Check for matches in our response dictionary
        for pattern, responses in self.responses.items():
            if re.search(pattern, user_input):
                return random.choice(responses)

        # If no match is found, return a default response
        return random.choice(self.default_responses)

    def start_chat(self):
        print(f"\n{self.name}: Hello! I'm {self.name}, your friendly chatbot. Type 'bye' to exit.")

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['bye', 'goodbye', 'exit']:
                print(f"\n{self.name}: {self.get_response(user_input)}")
                break

            response = self.get_response(user_input)
            print(f"\n{self.name}: {response}")


if __name__ == "__main__":
    # Create a new chatbot instance
    bot_name = "PyBot"
    bot = ChatBot(bot_name)

    # Check if we should run in demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run in demo mode with predefined inputs
        print(f"\n{bot_name}: Hello! I'm {bot_name}, your friendly chatbot. This is a DEMO mode.")

        demo_inputs = [
            "hello",
            "what is your name",
            "how are you",
            "tell me a joke",
            "what time is it",
            "tell me a fact",
            "what can you do",
            "favorite color",
            "where are you from",
            "tell me a story",
            "what is the meaning of life",
            "do you dream",
            "are you human",
            "sing a song",
            "damn this is cool",
            "thanks for chatting",
            "bye"
        ]

        for user_input in demo_inputs:
            print(f"\nYou: {user_input}")
            response = bot.get_response(user_input)
            print(f"\n{bot_name}: {response}")
            time.sleep(1)  # Add a small delay between responses
    else:
        # Start the interactive chat
        bot.start_chat()
