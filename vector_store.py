
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from data_loader import load_documents, split_documents  
load_dotenv()

os.environ["GOOGLE_API_KEY"] = "AIzaSyAstWNeBV1Hg5IFpvrY8zl_Qw8o1vSp_ks"  


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    api_key=os.getenv("GOOGLE_API_KEY"),
    request_timeout=30
)

VECTOR_DB_PATH = "chroma_db"  
def process_and_store_data(documents): #process and store docs into vectorstore
    if not documents:
        print("no docs recieved for processing, error")
        return None

    print(f"processing {len(documents)} documents...")

    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=VECTOR_DB_PATH  
    )

    print("documents stored successfully!")
    return vector_store

def load_vector_store(): #loads vector store from persistent storage
    if not os.path.exists(VECTOR_DB_PATH):
        print("chroma db not found")
        return None

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    stored_docs = vector_store.get(include=["documents"])
    print(f"loaded {len(stored_docs.get('documents', []))} documents from storage.")
    
    return vector_store

if __name__ == "__main__":
    
    docs = load_documents()
    chunked_docs = split_documents(docs)

    print(f"Documents before storing: {len(chunked_docs)}")  #debug 
    vector_store = process_and_store_data(chunked_docs)
    
    if vector_store:
        stored_docs = vector_store.get(include=["documents"]) 
        print(f"Stored Documents After Processing: {len(stored_docs.get('documents', []))}")
