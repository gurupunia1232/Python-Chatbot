import tkinter as tk
from tkinter import scrolledtext, ttk
import time
import threading
from chatbot import ChatBot

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyBot - Chatbot GUI")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # Create chatbot instance
        self.bot = ChatBot("PyBot")
        
        # Create and configure the chat display area
        self.create_widgets()
        
        # Welcome message
        self.display_bot_message("Hello! I'm PyBot, your friendly chatbot. How can I help you today?")
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat history display
        self.chat_history = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            bg="white", 
            font=("Arial", 11),
            width=50, 
            height=25
        )
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_history.config(state=tk.DISABLED)
        
        # Input area frame
        input_frame = tk.Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Message input field
        self.message_entry = tk.Entry(
            input_frame, 
            font=("Arial", 11),
            width=45
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.focus()
        
        # Send button
        send_button = ttk.Button(
            input_frame, 
            text="Send", 
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT)
        
        # Demo mode button
        demo_button = ttk.Button(
            main_frame, 
            text="Run Demo", 
            command=self.run_demo
        )
        demo_button.pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def display_user_message(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"\nYou: {message}\n", "user_message")
        self.chat_history.tag_configure("user_message", foreground="#0000CC")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)
    
    def display_bot_message(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"\nPyBot: {message}\n", "bot_message")
        self.chat_history.tag_configure("bot_message", foreground="#CC0000")
        self.chat_history.see(tk.END)
        self.chat_history.config(state=tk.DISABLED)
    
    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Clear the entry field
        self.message_entry.delete(0, tk.END)
        
        # Display user message
        self.display_user_message(message)
        
        # Check for exit command
        if message.lower() in ['bye', 'goodbye', 'exit']:
            self.display_bot_message(self.bot.get_response(message))
            self.status_var.set("Closing in 2 seconds...")
            self.root.after(2000, self.root.destroy)
            return
        
        # Get and display bot response (in a separate thread to keep UI responsive)
        self.status_var.set("PyBot is thinking...")
        threading.Thread(target=self.get_bot_response, args=(message,), daemon=True).start()
    
    def get_bot_response(self, message):
        # Simulate thinking time for more natural interaction
        time.sleep(0.5)
        response = self.bot.get_response(message)
        
        # Update UI in the main thread
        self.root.after(0, lambda: self.display_bot_response(response))
    
    def display_bot_response(self, response):
        self.display_bot_message(response)
        self.status_var.set("Ready")
    
    def run_demo(self):
        # Disable the demo button during demo
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget["text"] == "Run Demo":
                widget.config(state=tk.DISABLED)
        
        # Demo inputs
        demo_inputs = [
            "hello",
            "what is your name",
            "how are you",
            "tell me a joke",
            "what time is it",
            "tell me a fact",
            "what can you do",
            "favorite color",
            "calculate 5+7*3",
            "tell me a story",
            "thanks for chatting"
        ]
        
        # Start demo in a separate thread
        threading.Thread(target=self.run_demo_sequence, args=(demo_inputs,), daemon=True).start()
    
    def run_demo_sequence(self, demo_inputs):
        for i, user_input in enumerate(demo_inputs):
            # Display user message
            self.root.after(i * 4000, lambda msg=user_input: self.display_user_message(msg))
            
            # Get bot response
            response = self.bot.get_response(user_input)
            
            # Display bot response after a short delay
            self.root.after(i * 4000 + 1000, lambda resp=response: self.display_bot_message(resp))
        
        # Re-enable the demo button after demo
        self.root.after(len(demo_inputs) * 4000, self.enable_demo_button)
    
    def enable_demo_button(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button) and child["text"] == "Run Demo":
                        child.config(state=tk.NORMAL)
        self.status_var.set("Demo completed")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
