# Chat History with MessagesPlaceholder

import os 

from pydantic import SecretStr
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("The OPENAI API KEY is not set in your environment. Check your imports and .env file")

# Create a prompt template with history
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# Create a history object
history = ChatMessageHistory()

# User Speaks
history.add_message(HumanMessage(content="Hi, who won the Football World Cup in 2022?"))

# AI Speaks
history.add_message(AIMessage(content="Of course! Argentina won the World Cup in 2022?"))

# User Speaks
history.add_message(HumanMessage(content="Which team was playing opposite to Argentina?"))

# AI Speaks
history.add_message(AIMessage(content="It was contested between Argentina and France with a tie of 3-3, finally Argentina won 4-2 on penalties."))

# Initialize the LLM
llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2, api_key=SecretStr(OPENAI_API_KEY))

output_parser = StrOutputParser()

# Create LCEL chain
chain = prompt | llm | output_parser

response = chain.invoke({"history":history.messages, "question":"Who was captain of the winning team at the event and who was the Man of the match?"})
print(response)