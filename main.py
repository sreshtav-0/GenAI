from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage, trim_messages
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr
import os
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Langchain is a framework for developing applications powered by LLMs."),
    Document(page_content="LCEL (Langchain Expression language) enables composable chain building."),
    Document(page_content="Vector stores like FAISS, Chroma, Qdrant enable semantic search."),
    Document(page_content="RAG combines retrieval with generation for grounded responses."),
    Document(page_content="RunnablePassthrough passes inputs unchanged through the chain.")
]

splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=0)
splits = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(splits, embedding = embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

class SessionStore:
    def __init__(self):
        self.store : dict[str, ChatMessageHistory] = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store.setdefault(session_id, ChatMessageHistory())
        return self.store[session_id]

store = SessionStore()

trimmer = trim_messages(
    max_tokens=400,
    strategy="last",
    token_counter=ChatOpenAI(model = "gpt-5-nano", temperature=0.2),
    include_system=True,
    allow_partial=True,
    start_on="human"
)

def format_docs(docs:List[Document])->str:
    return "\n\n".join([doc.page_content for doc in docs])

def extract_question(input_dict: dict) -> str:
    return input_dict.get_question()

def create_contextualized_question(input_dict: dict) -> str:
    messages = input_dict.get("chat_history", [])
    question = input_dict.get("question", "")

    if not messages:
        return question
    
    recent = messages[:-4]

    history_text = "\n".join(
        f"{"Human" if isinstance(msg, HumanMessage) else "AI"}: {msg.content}" 
        for msg in recent if isinstance(msg, (HumanMessage, AIMessage))
    )

    return(
        "Use the conversation context to interpret the user's intent. \n"
        f"Conversation history:\n{history_text}\n\n"
        f"Question: {question}\n"
    )

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant with access to a knowledge base."
            "Use the provided context to answer questions accurately."
            "If the context is insufficient, say you're unsure."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            "human", 
            """
            Context from the knowledge base: {context}
            Question: {question}
            """
        )
    ]
)

retrieval_chain = (
    RunnableLambda(create_contextualized_question) | retriever | RunnableLambda(format_docs)
)

chain = (
    RunnablePassthrough.assign(chat_history=RunnableLambda(lambda x: trimmer.invoke(x.get("chat_history", []) or [])),
    context = retrieval_chain)
    | prompt | llm | StrOutputParser()
)

chain_with_history = RunnableWithMessageHistory(
    chain, get_session_history=store.get_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

class ChatInterface:
    def __init__(self, session_id:str="default")->None:
        self.session_id = session_id
        self.config = {"configurable": {"session_id":self.session_id}}

    def chat(self, message:str)->str:
        return chain_with_history.invoke({"question": message}, config=self.config)
    
    def get_history(self)->List[BaseMessage]:
        return store.get_session_history(self.session_id).messages
    
    def clear_history(self)->None:
        store.get_session_history(self.session_id).clear()

if __name__ == "__main__":
    # Terminal Colors
    RED = "\033[31;1m"
    GREEN = "\033[32;1m"
    YELLOW = "\033[33;1m"
    BLUE = "\033[34;1m"
    PURPLE = "\033[35;1m"
    CYAN = "\033[36;1m"
    WHITE = "\033[37;1m"
    ORANGE = "\033[38;5;208m"
    TEAL = "\033[38;5;37m"
    RESET = "\033[0;0m"

    print(f"{GREEN}Welcome to the Langchain Chat Interface!\n{ORANGE}Type 'quit' or 'exit' to exit, 'history' to view, and 'clear' to clear history.")
    chat = ChatInterface(session_id="user123")
    while True:
        user_input = input(f"{CYAN}You: {RESET}")
        if user_input.lower() in ["quit", "exit"]:
            print(f"{YELLOW}Goodbye!{RESET}")
            break
        elif user_input.lower() == "history":
            history = chat.get_history()
            print(f"{BLUE}Chat History:{RESET}")
            for msg in history:
                role = "You" if isinstance(msg, HumanMessage) else "Assistant"
                print(f"{TEAL}{role}: {msg.content}{RESET}")
        elif user_input.lower() == "clear":
            chat.clear_history()
            print(f"{RED}Chat history cleared.{RESET}")
        elif not user_input:
            print(f"{YELLOW}Please enter a valid message.{RESET}")

        response = chat.chat(user_input)
        print(f"{PURPLE}Assistant: {response}")

        