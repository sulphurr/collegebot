from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from search import search_room, load_vector_store
from db import get_db_connection
from nlp import categorize_query
from faculty import handle_faculty_query
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
import os
from langchain_community.vectorstores import Chroma
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
vector_store = load_vector_store()

def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

#app.py
@app.get("/query", response_class=PlainTextResponse)
async def handle_query(query: str, db=Depends(get_db)):
    #redirect based on category
    try:
        cleaned_query = query.lower().strip()
        #Categorize query using Gemini
        category = categorize_query(cleaned_query)
        logger.info(f"Categorized query as: {category}")
        if category == "small_talk":
            return handle_small_talk(cleaned_query)
        elif category == "room":
            return search_room(query, vector_store)  # Pass preloaded vector store
        elif category == "faculty":
            return handle_faculty_query(query, db)
        return "I'm not sure how to categorize this query."
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return "An error occurred while processing your query. Please try again."

def handle_small_talk(query: str) -> str:
    try:
        gemini = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )
        prompt = (
            "You are a helpful and professional college assistant. "
            "Respond naturally and friendly to this casual conversation: "
            "Always end with asking if they need help with faculty or room query"
            "Refrain from asking too many questions, stick to your role"
            f"'{query}'"
        )

        reply = gemini.invoke(prompt)
        return reply.content.strip() if reply and reply.content else "I'm here to help! What would you like to know?"
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "I'm here to help! What would you like to know?"
