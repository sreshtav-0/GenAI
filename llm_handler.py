import base64
from PIL import Image
from typing import Dict, List, Optional
from groq import Groq
from openai import OpenAI
from google import genai
from google.genai import types
import io

def encode_image(image_file)->str:
    return base64.b64encode(image_file.read()).decode("utf-8")

def format_messages_for_provider(messages:List[Dict], provider:str)->List[Dict]:
    match provider:
        case "gemini":
            # Gemini uses "user" and "model" roles
            formatted = []
            for msg in messages:
                role = "model" if msg["role"] == "assistant" else "user"
                formatted.append({"role": role, "parts": [msg['content']]})
            return formatted
    return messages

class LLMHandler:
    def __init__(self, provider:str, api_key:str, model:str, temperature:float=0.7,
                 max_tokens:int=1024):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        match provider:
            case "groq":
                self.client = Groq(api_key=api_key)

            case "openai":
                self.client = OpenAI(api_key=api_key)
            
            case "gemini":
                self.client = genai.Client(api_key=api_key)
            
            case _:
                raise ValueError(f"Invalid provider: {provider}")
    
    def chat(self, messages:List[Dict], image_data:Optional[str]=None)->str:
        match self.provider:
            case "groq":
                return self.groq_chat(messages, image_data)
            case "openai":
                return self.openai_chat(messages, image_data)
            case "gemini":
                return self.gemini_chat(messages, image_data)
            case _:
                raise ValueError(f"Invalid provider: {self.provider}")
    
            
    def groq_chat(self, messages:List[Dict], image_data:Optional[str]=None)->str:
        model = "meta-llama/llama-4-scout-17b-16e-instruct" if image_data else self.model

        chat_messages = messages.copy()
        if image_data:
            chat_messages[-1] = {
                "role":"user",
                "content": [
                    {"type" : "text", "text" : messages[-1]['content']},
                    {"type" : "image_url",
                     "image_url" : {"url": f"data:image/jepg;base64, {image_data}"}
                    }
                ]
            }
        response = self.client.chat.completions.create(
            model = model,
            messages = chat_messages,
            temperature = self.temperature,
            max_tokens = self.max_tokens,
        )

        return response.choices[0].message.content

    def openai_chat(self, messages:List[Dict], image_data:Optional[str]=None)->str:
        model = "gpt-4o" if image_data else self.model

        chat_messages = messages.copy()
        if image_data:
            chat_messages[-1] = {
                "role":"user",
                "content": [
                    {"type" : "text", "text" : messages[-1]['content']},
                    {"type" : "image_url",
                     "image_url" : {"url": f"data:image/jepg;base64, {image_data}"}
                    }
                ]
            }
        response = self.client.chat.completions.create(
            model = model,
            messages = chat_messages,
            temperature = self.temperature,
            max_completion_tokens = self.max_tokens,
        )

        return response.choices[0].message.content
    
    def gemini_chat(self, messages: List[Dict], image_data: Optional[str] = None) -> str:
        """Handle Gemini API calls with google.genai"""
        if image_data:
            # For vision, create prompt with image
            import io
            from PIL import Image
            
            # Decode base64 to image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Get the last user message text
            prompt = messages[-1]["content"]
            
            # Create content parts
            parts = [prompt, types.Part.from_image(image)]
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=parts,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            return response.text
        else:
            # Text-only chat - convert messages to Gemini format
            gemini_messages = []
            for msg in messages:
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_messages.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=gemini_messages,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens
                )
            )
            return response.text
        
