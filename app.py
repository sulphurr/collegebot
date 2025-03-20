#app.py
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from search import search_room
from db import get_db_connection
from nlp import categorize_query
from faculty import handle_faculty_query
from gemini_utils import rephrase_with_gemini
from langchain_google_genai import ChatGoogleGenerativeAI


app = FastAPI()

def get_db():
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

@app.get("/query", response_class=PlainTextResponse)
async def handle_query(query: str, db=Depends(get_db), vector_store=None):
    """Handle queries using Gemini categorization and modular components."""
    try:
        # Clean the query
        cleaned_query = query.lower().strip()
        
        # Create Gemini query for categorization
        category_query = GoogleGenerativeAIQuery(
            model="gemini-pro",
            api_key=os.getenv("GEMINI_API_KEY"),
            request_timeout=30
        )
        
        # Determine query category
        categories = {
            "room": VECTOR_STORES['rooms'].similarities(cleaned_query)
        }
        
        max_category = max(categories.items(), key=lambda x: x[1])
        
        if max_category[1] < 0.3:  # Threshold for confidence
            return handle_small_talk(cleaned_query)
            
        # Handle based on category
        if max_category[0] == "room":
            return search_room(query, vector_store)
        else:
            # Faculty query handling
            return handle_faculty_query(query, db)
            
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return "An error occurred while processing your query. Please try again."

def handle_small_talk(query: str) -> str:
    """Handle casual conversations using Gemini directly."""
    try:
        # Create Gemini query for small talk
        category_query = GoogleGenerativeAIQuery(
            model="gemini-pro",
            api_key=os.getenv("GEMINI_API_KEY"),
            request_timeout=30
        )
        
        # Prompt for small talk response
        prompt = (
            "You are a helpful and professional college assistant. "
            "Respond naturally and friendly to this casual conversation: "
            f"'{query}'"
        )
        
        # Get Gemini response
        reply = category_query.generate_content(prompt)
        if reply and hasattr(reply, "text"):
            return reply.text.strip()
        logger.warning("Gemini response was empty or invalid")
        return "I'm here to help! What would you like to know about faculty schedules or rooms?"
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "I'm here to help! What would you like to know about faculty schedules or rooms?"