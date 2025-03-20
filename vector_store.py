# vector_store.py
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

# Ensure API key is set
os.environ["GOOGLE_API_KEY"] = "AIzaSyCAkq8zlrzoSM-HUnGP0fURsPSA6txOifE"  # Replace with your key


# Force Gemini to use API Key instead of ADC
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    api_key=os.getenv("GOOGLE_API_KEY"),
    request_timeout=30
)

VECTOR_DB_PATH = "chroma_db"  # Persisted database folder

def process_and_store_data(documents):
    

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=os.getenv("GEMINI_API_KEY"),
        request_timeout=30  # Increase timeout to 30 seconds
    )

    
    # Chroma automatically persists data now
    vector_store = Chroma.from_documents(
        documents, 
        embeddings, 
        persist_directory=VECTOR_DB_PATH
    )
    
    return vector_store