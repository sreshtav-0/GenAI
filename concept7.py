import concept6 as c6

from typing import Optional
from langchain_core.messages import BaseMessage

def fetch_history_messages(session_id:str)->Optional[list[BaseMessage]]:
    try:
        hist = c6.store[session_id]
        return hist.messages
    except KeyError:
        return []
    

def fetch_history_as_tuples(session_id:str)->list[tuple[str, str]]:
    hist = c6.store.get(session_id)

    if not hist:
        return []
    
    output = []

    for msg in hist.messages:
        role = getattr(msg, "role", "unknown")
        content = getattr(msg, "content", "unknown")
        output.append((role, content))

    return output


def clear_history(session_id:str)->None:
    if session_id in c6.store:
        c6.store.pop(session_id)


def list_sessions()->list[str]:
    return list(c6.store.keys())


if __name__ == "__main__":    
    c6.with_history.invoke({"input": "Hi, my name is Mira Maruti. I was a senior software engineer at OpenAI. I have now created a new a new startup called Thinking Machine Lab in Feburary 2025."}, config=c6.cfg2)

    chat2_history = fetch_history_messages("chat2")
    print(chat2_history)

    clear_history("chat2")

    chat2_history = fetch_history_messages("chat2")
    print(chat2_history)