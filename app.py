# app.py

from fastapi import FastAPI
from data_loader import load_documents, split_documents
from vector_store import process_and_store_data
from fastapi.responses import PlainTextResponse
from search import search_room
import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware



# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Load and process data
docs = load_documents()
split_docs = split_documents(docs)
vector_store = process_and_store_data(split_docs)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/search")
def get_room_info(query: str):
    """Return room information using the search engine and Gemini for rephrasing."""
    results = search_room(query, vector_store)
    cleaned_result = results.replace("**", "").split(": ", 1)[-1]
    if "not found" in cleaned_result.lower():
        return f"Sorry, I couldn't find a room for '{query}'. Please check the code or spelling."
    else:
        return PlainTextResponse(content=cleaned_result)
