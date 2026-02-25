import os
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

import fitz
import chromadb

from google import genai
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains.retrieval import RetrievalOA
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Terminal Colors
RED = "\033[31;1m"
GREEN = "\033[32;1m"
YELLOW = "\033[33;1m"
BLUE = "\033[34;1m"
PURPLE = "\033[35;1m"
CYAN = "\033[36;1m"
TEAL = "\033[38;5;37m"
WHITE = "\033[37;1m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0;0m"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI API KEY found missing. Please check your .env file.")

class ChromaRAG:
    def __init__(self, gemini_api_key:Optional[str]=None, persist_directory:Optional[str]=None) -> None:
        self.api_key = gemini_api_key
        if not self.api_key:
            raise ValueError("Gemini API Key is required. Set GEMINI_API_KEY in env file.")
        
        self.embedding_model = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001", google_api_key = self.api_key)
        self.llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature=0.3, 
                                          api_key = self.api_key)
        self.persist_directory = persist_directory
        self.collection_name = "Chroma_PDF_Store"
        self._initialize_chromadb()
        
        self.vectorstore:Optional[Chroma] = None
        self.qa_chain:Optional[RetrievalOA] = None
        self.current_document:Optional[Document] = None
        self.document_chunks = []

    def _initialize_chromadb(self):
        if self.persist_directory:
            self.chroma_client = chromadb.PersistentClient(
                path = self.persist_directory, 
                settings = Settings(anonymized_telemetry = False)
            )
            print(f"{BLUE}Using persistent ChromaDB storage: {self.persist_directory}")
        else:
            self.chroma_client = chromadb.EphemeralClient(
                settings = Settings(anonymized_telemetry = False)
            )
            print(f"{CYAN}Using in-memory ChromaDB storage")

    def extract_text_from_pdf(self, pdf_path:str)->str:
        try:
            doc = fitz.open(pdf_path)
            text_content = ""

            for page_num in range(0, len(doc)):
                page = doc.load_page(page_num)
                text_content += f"\n--- Page {page_num + 1} ---\n"
                text_content += page.get_text()

            doc.close()
            return text_content
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
    def load_process_pdf(self, pdf_path:str, chunk_size:int=1000, 
                         chunk_overlap:int=225)->int:
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF File Not Found: {pdf_path}")
        
        print(f"{PURPLE} Loading PDF... {pdf_path}")

        pdf_text = self.extract_text_from_pdf(pdf_path)

        if not pdf_text.strip():
            raise ValueError("No text content found in the PDF")
        
        document = Document(
            page_content = pdf_text,
            metadata = {"source":pdf_path, "type": "pdf"}
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            separators = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        self.document_chunks = text_splitter.split_documents([document])
        print(f"{YELLOW}Created {len(self.document_chunks)} text chunks.")

        try:
            self.chroma_client.delete_collection(name=self.collection_name)
        except Exception:
            print("Collections don't exist, which is fine.")

        self.vectorstore = Chroma(
            client = self.chroma_client,
            collection_name = self.collectiom_name,
            embedding_function = self.embedding_model
        )

        self.vectorstore.add_documents(self.document_chunks)
        print(f"{GREEN}Vector embeddings created and stored in ChromaDB")
        self.setup_qa_chain()
        self.current_document = pdf_path
        return len(self.document_chunks)

    def load_pdf_from_bytes(self, pdf_bytes:bytes, filename:str, chunksize:int=1000, chunk_overlap:int=250)->int:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_path = tmp_file.name

            try:
                result = self.load_process_pdf(tmp_path, chunksize, chunk_overlap)
                self.current_document = filename
                return result

            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    
    def _setup_qa_chain(self):
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized")
        
        retriever = self.vectorstore.as_retriever(
            search_type = "similarity",
            search_kwargs = {"k":4}
        )

        prompt_template = """
You are a helpful AI assistant for analyzing PDF documents.
Use the following pieces of context to answer the question. If you don't know the answer based on the context, just say that you don't know. Be conversational and helpful.
Context: {context}
Question: {question}
        
        
Answer:"""

        prompt = PromptTemplate(
            template = prompt_template,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type = "stuff",
            retriever = retriever,
            return_source_documents = True,
            chain_type_kwargs = {"prompt": prompt}
        )

    def ask_question(self, query:str)->Tuple[str, List[Document]]:
        if not self.qa_chain:
            raise ValueError("No document loaded. Please load a PDF first.")
        
        print(f"{YELLOW}\n Question: {query}")

        try:
            response = self.qa_chain.invoke({"query": query})
            answer = response["result"]
            sources = response.get("source_documents", [])
            print(f"Answer: {answer}")

            if sources:
                print(f"\n Based on {len(sources)} relevant sections")
                for i, doc in enumerate(sources, 1):
                    preview = doc.page_content[:150].replace("\n", " ")
                    if len(doc.page_content) > 150:
                        preview += "..."
                    print("f{i}. {preview}")
            return answer, sources
            
        except Exception as e:
            error_msg = f"Error processing question: {e}"
            print("f{error_msg}")
            return error_msg, []
        
    def get_document_info(self)->dict:
        if not self.current_document:
            return {"status": "No document loaded"}
        
        collection_info = {}
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            collection_info = {
                "collection_count": collection.count(),
                "collection_name": self.collection_name
            }
        
        except Exception:
            collection_info = {"collection_count":0, "collection_name":"Not found"}

        return {
            "document": self.current_document,
            "chunks": len(self.document_chunks),
            "vectorstore_initialized": self.vectorstore is not None,
            "qa_chain_ready": self.qa_chain is not None,
            "chromadb_info": collection_info,
            "persist_directory": self.persist_directory
        }
    
    def search_document(self, query:str, k:int = 3)->List[Document]:
        if not self.vectorstore:
            raise ValueError("No document loaded")
        
        return self.vectorstore.similarity_search(query, k=k)
    
    def search_with_scores(self, query:str, k:int=3)->List[Tuple[Document, float]]:
        if not self.vectorstore:
            raise ValueError("No document loaded")
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
    def list_collections(self)->List[str]:
        collections = self.chroma_client.list_collections()
        return [col.name for col in collections]
    
    def delete_collection(self, colection_name:Optional[str]=None)->bool:
        name = collection_name or self.collection_name
        try:
            self.chroma_client.delete_collection(name = name)
            print(f"Deleted collection: {name}")
            return True
        except Exception as e:
            print(f"Error deleting collection {name}:{e}")
            return False
        
    def main():
        print("An AI-powered PDF question-answering system using Google Gemini & ChromaDB")
        print("-" * 70)
    
        # Ask user about persistence
        use_persistence = input("💾 Do you want to persist embeddings to disk? (y/n): ").strip().lower() == 'y'
        persist_dir = None
    
        if use_persistence:
            persist_dir = input("📁 Enter persist directory (or press Enter for './chroma_db'): ").strip()
            if not persist_dir:
                persist_dir = "./chroma_db"
            Path(persist_dir).mkdir(parents=True, exist_ok=True)
    
        # Initialize the system
        try:
            pdf_talker = ChromaRAG(gemini_api_key=GEMINI_API_KEY,persist_directory=persist_dir)
            print("✅ System initialized successfully")
        
            if use_persistence:
                collections = pdf_talker.list_collections()
                if collections:
                    print(f"📂 Existing collections: {', '.join(collections)}")
        
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            return
    
        # Load PDF
        pdf_path = input("\n📁 Enter the path to your PDF file: ").strip()
    
        try:
            num_chunks = pdf_talker.load_and_process_pdf(pdf_path)
            print(f"✅ PDF loaded successfully! Created {num_chunks} chunks.")
        
            # Show document info
            info = pdf_talker.get_document_info()
            print(f"📊 ChromaDB collection '{info['chromadb_info']['collection_name']}' has {info['chromadb_info']['collection_count']} documents")
        
        except Exception as e:
            print(f"❌ Error loading PDF: {e}")
            return
    
        # Interactive Q&A loop
        print("\n💬 You can now ask questions about your PDF!")
        print("Commands:")
        print("  - Type your question normally")
        print("  - 'search <query>' - Just search without LLM answer")
        print("  - 'info' - Show document information")
        print("  - 'quit' or 'exit' - Stop the program")
        print("-" * 50)
    
        while True:
            try:
                user_input = input("\n❓ Your input: ").strip()
            
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
            
                if not user_input:
                    continue
            
                if user_input.lower() == 'info':
                    info = pdf_talker.get_document_info()
                    print("\n📊 Document Information:")
                    for key, value in info.items():
                        print(f"  {key}: {value}")
                    continue
            
                if user_input.lower().startswith('search '):
                    query = user_input[7:]  # Remove 'search ' prefix
                    results = pdf_talker.search_with_scores(query, k=3)
                    print(f"\n🔍 Search results for: '{query}'")
                    for i, (doc, score) in enumerate(results, 1):
                        preview = doc.page_content[:200].replace('\n', ' ')
                        if len(doc.page_content) > 200:
                            preview += "..."
                        print(f"  {i}. Score: {score:.4f}")
                        print(f"     {preview}")
                    continue
            
                # Regular question
                answer, sources = pdf_talker.ask_question(user_input)
                print(f"\n{'='*60}")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
    