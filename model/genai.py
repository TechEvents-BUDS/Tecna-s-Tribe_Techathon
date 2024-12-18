import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict
from together import Together

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEy")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")


class AI:
    def __init__(self, system_prompt: str):
        """
        Initialize the chatbot with a base system prompt.
        
        Args:
            system_prompt (str): The initial system instruction for the AI
        """
        # Initialize Together client
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, user_message: str) -> str:
        """
        Generate a response by adding the user message to conversation history 
        and calling the Together AI API.
        
        Args:
            user_message (str): The user's input message
        
        Returns:
            str: The AI's generated response
        """

        # Generate AI response
        try:
            response = self.model.generate_content(user_message)
            print(response.text)

            return response.text

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, there was an error processing your request."

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Retrieve the full conversation history.
        
        Returns:
            List[Dict[str, str]]: The conversation history
        """
        return self.messages

    def reset_conversation(self, system_prompt: Optional[str] = None):
        """
        Reset the conversation history.
        
        Args:
            system_prompt (Optional[str]): New system prompt to use. 
                                           If None, uses the original system prompt.
        """
        if system_prompt:
            self.messages = [{"role": "system", "content": system_prompt}]
        else:
            # Reset to initial state
            self.messages = [self.messages[0]]


import os
import openai

class Classify:
    def __init__(self, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"):
        self.client = openai.OpenAI(
            api_key=os.environ.get("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1"
        )
        self.model = model

    def generate_response(self, user_input):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a travel agent. Be descriptive and helpful."},
                {"role": "user", "content": user_input},
            ]
        )
        return response.choices[0].message.content
