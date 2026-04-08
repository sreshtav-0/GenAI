# Runnable with Message History - 
"""
+ Automatic message history management
+ Session-based conversations
+ History persistnace across invocations
"""
import os 

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import SecretStr

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")
 
store: dict[str, ChatMessageHistory] = {}

def get_session_history(session_id:str)->BaseChatMessageHistory:
    """
    Returing a ChatMessageHistory for a given session ID.
    If one does'nt exist, one will be created
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You're a helpful assistant. Be concise."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Initialize the LLM
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2, api_key=SecretStr(OPENAI_API_KEY))

# Creating the string output parser
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

with_history = RunnableWithMessageHistory(
    chain, 
    get_session_history=get_session_history,
    input_messages_key="input", # When the new term come in
    history_messages_key="history" # Where past turns are injected
)

cfg1 = {"configurable": {"session_id": "chat1"}}
cfg2 = {"configurable": {"session_id": "chat2"}}

if __name__ == "__main__":
    # Session-1
    response1 = with_history.invoke({"input":"Hi, my name is Sam Altman, and I'm the CEO of OpenAI. OpenAI is a company which focus on building Artifical General intelligence."}, config=cfg1)
    print("chat1:", response1)

    response2 = with_history.invoke({"input":"What's my name"}, config=cfg1)
    print("chat1:", response2)

    response3 = with_history.invoke({"input":"What does OpenAI focus on?"}, config=cfg1)
    print("chat1:", response3)

    print("----------------------------------------------------------------------")
    # Session-2
    response4 = with_history.invoke({"input": "Hi, my name is Mira Maruti. I was a senior software engineer at OpenAI. I have now created a new a new startup called Thinking Machine Lab in Feburary 2025."}, config=cfg2)
    print("Chat 2:", response4)

    response5 =  with_history.invoke({"input": "What does Thinking Machine Lab focuses upon"}, config=cfg2)
    print("Chat2:", response5)