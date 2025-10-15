import os 
import json
import asyncio

import httpx

from pprint import pprint
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

# Terminal Colors
RED = "\033[31;1m"
GREEN = "\033[32;1m"
YELLOW = "\033[33;1m"
BLUE = "\033[34;1m"
PURPLE = "\033[35;1m"
CYAN = "\033[36;1m"
WHITE = "\033[37;1m"
ORANGE = "\033[38;5;208m"

# Setting up the API 
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY") or ""

class ContextAwareGemini:
    def __init__(self, api_key:Optional[str]=None, model_name="gemini-2.5-pro") -> None:
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model_name = model_name 

        if not self.api_key:
            raise ValueError("Gemini API key is required! Set GEMINI_API_KEY in your environment")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.conversation_history = []

    def add_to_history(self, role:str, content:str)->None:
        self.conversation_history.append({
        "role":role, 
        "content": content
    })
        
    def format_message_for_gemini(self)->List[Dict[str, str]]:
        formatted_messages = []

        for message in self.conversation_history:
            if message["role"] == "user":
                formatted_messages.append({
                    "role": "user", 
                    "parts": [{"text": message["content"]}]
            })
            elif message["role"] in ["assistant", "model"]:
                formatted_messages.append({
                    "role": "model", 
                    "parts": [{"text": message["content"]}]
            })
        return formatted_messages
    
    async def get_response(self, user_input:str)->str:
        # Add user input to history 
        self.add_to_history("user", user_input)

        # Prepare the request payload 
        messages= self.format_message_for_gemini()

        # Adding system Instructions 
        if len(messages) == 1: # Only user message exist 
            system_message = {
                "role": "user", 
                "parts": [{"text": "You're a helpful chatbot. Maintain context awareness and provide helpful responses."}]
            }
            system_response = {
                "role": "model", 
                "parts": [{"text": "I understand. I'll be a helpful chatbot that maintains context awareness throughout our conversation."}]
            }

            messages.insert(0, system_message)
            messages.insert(1, system_response)

        # Construct the payload for Gemini API 
        payload = {
            "contents": messages, 
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95, 
                "maxOutputTokens": 1024
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }

        response_text = ""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                end_point = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
                response = await client.post(end_point, json=payload,
                headers={"Content-Type":"application/json"})
                response.raise_for_status()

                if response.status_code == 200:
                    response_data = response.json() 
                    if "candidates" in response_data and response_data["candidates"]:
                        candidate = response_data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            response_text = candidate["content"]["parts"][0]["text"]
                        else:
                            response_text = "No response generated"
                else:
                    error_details = response.text 
                    response_text = f"I could'nt generate a response this time.(Status {response.status_code})"
                    print(f"{RED}API Error: {response_text}-{error_details}")
        except httpx.TimeoutException:
            response_text = "Request timed out. Please try again later."
            print(f"{RED}Error: Requested Timeout")
        except httpx.RequestError as e:
            response_text = "I could'nt connect to the service. Check you Internet bandwidth."
            print(f"{RED}Error: {e}")
        except json.JSONDecodeError as e:
            response_text = "I receive an invalid JSON response. Please try again!"
            print(f"{RED}Error: Invalid JSON response.")
        except Exception as e:
            response_text = "An unexpected error occurred!"
            print(f"{RED}Error: {e}")

        self.add_to_history("assistant", response_text)
        return response_text 
    
    async def start_conversation(self)->None:
        print(f"{YELLOW}Starting the conversation with GEMINI. Type `exit`, `quit` or `finish` to end the conversation.")

        while True:
            try:
                user_input = input(f"{PURPLE}You: ").strip()

                if user_input.lower() in ["exit", "quit", "finish"]:
                    print(f"{CYAN}Ending Conversation!")
                    break
                if not user_input:
                    print(f"{RED}Please send a valid message.")
                    continue 

                print(f"{GREEN}Thinking...")
                response = await self.get_response(user_input)
                print(f"{BLUE}GEMINI: {response}")
            except KeyboardInterrupt:
                print(f"{CYAN}Conversation Interupted! Goodbye👋")
            except Exception as e:
                print(f"{RED}An error occurred: {e}")

    def get_conversation_history(self)->List[Dict[str, str]]:
        return self.conversation_history
    
    def delete_history(self)->None:
        self.conversation_history = []

    async def get_single_response(self, message:str)->str:
        return await self.get_response(message)
    

if __name__ == "__main__":
    chatbot = ContextAwareGemini()
    menu = f"""{WHITE}
1. Streamming Conversation 
2. Single Conversation 
3. Get Conversation History 
4. Delete Conversation History 
5. Exit
"""
    while True:
        print(menu)
        choice = input("{ORANGE}Enter your choice: ").strip()

        if choice == "1":
            asyncio.run(chatbot.start_conversation())
        elif choice == "2":
            user_input = input(f"{PURPLE}You: ").strip()
            asyncio.run(chatbot.get_single_response(message=user_input))
        elif choice == "3":
            history = chatbot.get_conversation_history()
            if history:
                print(f"{YELLOW}Conversation History:")
                for message in history:
                    print(f"{ORANGE}{message['role'].upper()}: {message['content']}")
            else:
                print(f"{RED}No conversation history found.")
        elif choice == "4":
            chatbot.delete_history()
            print(f"{GREEN}Conversation history deleted successfully!")
        elif choice == "5":
            break
