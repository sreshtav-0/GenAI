import os 
import json 
import asyncio 

import httpx 

from pprint import pprint
from typing import Dict, List, Optional

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


class ContextAwareOpenAI:
    def __init__(self, api_key: str, model_name:str="gpt-4o-mini") -> None:
        self.api_key =  api_key
        self.model_name = model_name 

        if not self.api_key:
            raise ValueError("OPENAI API key is required! Check your .env file") 
        
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.conversation_history = []

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } 

    def add_to_history(self, role:str, content:str)->None:
        self.conversation_history.append({"role":role, "content": content})

    def format_messages_for_openAI(self)->List[Dict[str, str]]:
        return self.conversation_history
    
    async def get_response(self, user_input:str)->str:
        # Add user input to history 
        self.add_to_history("user", user_input)

        context_prompt = {
            "role": "system",
            "content": "You're a helpful chatbot. Maintain context and provide helpful responses."
        }

        if context_prompt not in self.conversation_history:
            messages = [context_prompt]  + self.format_messages_for_openAI()
        else:
            messages = self.format_messages_for_openAI() 

        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.95, 
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url=self.base_url,
                    json=payload,
                    headers=self.headers
                )

                response.raise_for_status()

                if response.status_code == 200:
                    response_data = response.json()
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        choice = response_data["choices"][0]
                        if "message" in choice and "content" in choice["message"]:
                            response_text = choice["message"]["content"].strip()
                        else:
                            response_text = "I can't generate a proper response"
                    else:
                        response_text = "No response generated!"
                else:
                    error_details = response.text 
                    response_text = f"I could'nt generate a response this time. (Status: {response.status_code})"
                    print(f"{RED}API Error: {response_text}->{error_details}")
        
        except httpx.TimeoutException:
            response_text = "Request timed out. Please try again!"
            print(f"{RED}Error: Requested Timeout")
        except httpx.RequestError as e:
            response_text = "I could'nt connect to the service. Please check your internet connection."
            print(f"{RED}Request Error: {e}")
        except json.JSONDecodeError:
            response_text = "I receive an invalid JSON response.Please try again!"
            print(f"{RED}Error: Invalid JSON response.")
        except Exception as e:
            response_text = "An unexpected error occurred!"
            print(f"{RED}Unexpected Error: {str(e)}")

        self.add_to_history("assistant", response_text)
        return response_text
    
    async def start_conversation(self)->None:
        print(f"{BLUE}Starting the conversation with OPENAI. Type `exit`, `quit` or `finish` to end the conversation.")

        while True:
            try:
                user_input = input(f"{WHITE}You: ").strip()

                if user_input.lower() in ["exit", "quit", "finish"]:
                    print(f"{CYAN}Ending Conversation!")
                    break
                if not user_input:
                    print(f"{RED}Please send a valid message.")
                    continue 

                print(f"{GREEN}Thinking...")
                response = await self.get_response(user_input)
                print(f"{PURPLE}OPENAI: {response}")
            except KeyboardInterrupt:
                print(f"{CYAN}Conversation Interupted! Goodbye👏")
            except Exception as e:
                print(f"{RED}An error occurred!-{str(e)}")

    def get_conversation_history(self)->List[Dict[str, str]]:
        return self.conversation_history
    
    def clear_conversation_history(self)->None:
        self.conversation_history = []

    async def get_single_response(self, message:str)->str:
        return await self.get_response(message)
    

if __name__ == "__main__":
    chatbot = ContextAwareOpenAI(api_key=os.getenv("OPENAI_API_KEY_VS"))
    menu = f"""{WHITE}
1. Streamming Conversation 
2. Single Conversation 
3. Get Conversation History 
4. Delete Conversation History 
5. Exit
"""
    while True:
        print(menu)
        choice = input(f"{ORANGE}Enter your choice: ").strip()

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
            chatbot.clear_conversation_history()
            print(f"{GREEN}Conversation history deleted successfully!")
        elif choice == "5":
            break
