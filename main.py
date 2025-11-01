import asyncio
import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv
import httpx

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

class ContextAwareGroq:
    def __init__(self, groq_key: str):
        self.api_key = os.getenv(groq_key)
        self.model = "openai/gpt-oss-120b"
        self.conversation_history: List[Dict[str, str]] = []
        if not self.api_key:
            raise ValueError("GROQ_KEY environment variable not set.")
        
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.available_model = [
            "openai/gpt-oss-120b",
            "groq/compound",
            "qwen/qwen3-32b",
            "llama-3.3-70b-versatile",
            "moonshotai/kimi-k2-instruct-0905",
            "meta-llama/llama-guard-4-12b"
        ]

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def add_to_history(self, role: str, content: str) -> None:
        self.conversation_history.append({"role": role, "content": content})
    
    def format_messages(self) -> List[Dict[str, str]]:
        return self.conversation_history

    def set_model(self, model: str) -> None:
        if model in self.available_model:
            self.model = model
            print(f"{GREEN}Model set to {model}")
    
    async def get_response(self, user_input: str) -> str:
        self.add_to_history("user", user_input) 

         # Context Prompt 
        context_prompt = {
            "role": "system",
            "content": "You are a helpful assistant that provides accurate and concise information based on the user's input and the conversation history. "
            "Always refer to previous messages to maintain context and coherence in your responses. "
            "If the information seems out of bounds, politely ask for clarification or more details."
        }    

        messages = [context_prompt] + self.format_messages()

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 0.95,
            "stream": True
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", self.base_url, json=payload, headers=self.headers) as response:
                    response.raise_for_status() 
                    response_text = "" 
                    async for chunk in response.aiter_lines():
                        if chunk.startswith("data:"):
                            data = chunk[len("data:"):].strip()
                            if data == ["DONE"]:
                                break
                            try:
                                chunk_json = json.loads(data)
                                if "choices" in chunk_json and len(chunk_json["choices"]) > 0:
                                    delta = chunk_json["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        content = delta["content"]
                                        response_text += content
                            except json.JSONDecodeError:
                                continue
        except httpx.TimeoutException:
            response_text = "Request timed out. Please try again later."
            return f"{RED}{response_text}"
        except httpx.RequestError as e:
            response_text = "An error occurred while making the request: "
            return f"{RED}{response_text}{e}"
        except json.JSONDecodeError:
            response_text = "Failed to parse the response. Please try again later."
            return f"{RED}{response_text}"
        except Exception as e:
            response_text = "An unexpected error occurred: "
            return f"{RED}{response_text}{e}"
        
        self.add_to_history("assistant", response_text)
        return response_text
    
    async def start_conversation(self) -> None:
        print(f"{YELLOW}Starting conversation with GROQ using model: {self.model}. Type 'exit' to end the conversation.{WHITE}")
        print(f"{ORANGE}Commands 'models' to see available models, and 'clear' to clear history.{WHITE}")

        while True:
            try:
                user_input = input(f"{CYAN}You: {WHITE}")
                if user_input.lower() == "exit":
                    print(f"{YELLOW}Ending conversation. Goodbye!{WHITE}")
                    break
                elif user_input.lower() == "clear":
                    self.clean_history()
                    print(f"{GREEN}Conversation history cleared.{WHITE}")
                    continue
                elif user_input.lower() == "models":
                    print(f"{PURPLE}Available Models:{WHITE}")
                    for index, model in enumerate(self.available_model, start=1):
                        print(f"{BLUE}{index}:{model}{WHITE}")
                    model_swap = int(input(f"{CYAN}Enter the model name to switch or press Enter to continue with current model - {self.model}: {WHITE}"))
                    if 1 <= model_swap <= len(self.available_model):
                        self.model = self.available_model[model_swap - 1]
                        print(f"{GREEN}Model swapped to: {self.model}")
                    else:
                        print(f"{YELLOW}Invalid model selection. Type 'models' to see available models. Continuing with current model.{WHITE}")
                        continue
                if not user_input:
                    print(f"{RED}Input cannot be empty. Please enter a valid message.{WHITE}")

                print(f"{YELLOW}GROQ is typing...{WHITE}")
                response = await self.get_response(user_input)
                print(f"{GREEN}GROQ - {self.model}: {response}{WHITE}", flush=True)
            except KeyboardInterrupt:
                print(f"\n{YELLOW}Conversation interrupted. Goodbye!{WHITE}")
            except Exception as e:
                print(f"{RED}An error occurred: {e}{WHITE}")
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history
    
    def clean_history(self) -> None:
        self.conversation_history = []

if __name__ == "__main__":
    groq_bot = ContextAwareGroq(groq_key="GROQ_KEY")
    asyncio.run(groq_bot.start_conversation())
    