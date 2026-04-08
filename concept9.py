import os

from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from pydantic import SecretStr

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

# Initialize LLM
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2, 
    api_key=SecretStr(OPENAI_API_KEY))

trimmer = trim_messages(
    max_tokens=200,
    strategy="last",
    token_counter=llm,
    include_system=True,
    allow_partial=True,
    start_on="human"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a helpful assistant. Be concise and answer to the best of your ability in {language}."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = ({"history": itemgetter("history") | trimmer,
          "language": itemgetter("language"),
          "input": itemgetter("input")} | prompt | llm)

store : dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store.setdefault(session_id, ChatMessageHistory())
    return store[session_id]

with_history = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="input", history_messages_key="history")

config1 = {"configurable": {"session_id": "chat1"}}
history1 = get_session_history("chat1")

seed = [
    HumanMessage(content="Hi, my name is Mario from Super Mario"),
    AIMessage(content="Hello, Mr. Mario from Super Mario. If you any assistant in your plumbing or your mission in saving Princess Peach."),
    HumanMessage(content="What more stuff you know about me?"),
    AIMessage(content="I know that you first appear in the game `Donkey Kong`. And, you are name after real estate developer Mario Segale."),
    HumanMessage(content="Where do I live?"),
    AIMessage(content="You live in the Mushroom Kingdom.")
]

for message in seed:
    if isinstance(message, HumanMessage):
        history1.add_user_message(message.content)
    elif isinstance(message, AIMessage):
        history1.add_ai_message(message.content)

response1 = with_history.invoke({"input": "What is my name?", "language": "English"}, config=config1)
print(response1)

response2 = with_history.invoke({"input": "Where do I live?", "language": "English"}, config=config1)
print(response2)