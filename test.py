import os 
import asyncio
import httpx 
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("OPENAI_API_KEY_VS"))
async def test():
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY_VS')}",
        "Content-type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ]
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        print(r.status_code, r.text)

asyncio.run(test())