#nlp.py
from langchain_google_genai import GoogleGenerativeAIQuery
from typing import Dict, Optional
import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def categorize_query(query: str) -> str:
    """
    Categorize the query into small talk, room query, or faculty query.
    
    Args:
        query (str): The user's query to be categorized
        
    Returns:
        str: The category of the query ("small_talk", "room_query", or "faculty_query")
    """
    try:
        # Clean the query
        cleaned_query = query.lower().strip()
        
        # Create Gemini query for categorization
        category_query = GoogleGenerativeAIQuery(
            model="gemini-pro",
            api_key=os.getenv("GEMINI_API_KEY"),
            request_timeout=30
        )
        
        # Define categorization prompt
        prompt = (
            "Categorize this query into one of three categories:\n\n"
            "1. small_talk: Casual conversation, greetings, or general chat\n"
            "2. room_query: Questions about room locations, facilities, or directions\n"
            "3. faculty_query: Questions about faculty members, their schedules, or staffrooms\n\n"
            f"Query to categorize: '{cleaned_query}'\n\n"
            "Return exactly one category name from the above options."
        )
        
        # Get Gemini's categorization
        reply = category_query.generate_content(prompt)
        if reply and hasattr(reply, "text"):
            category = reply.text.strip()
            logger.info(f"Query categorized as: {category}")
            return category
        logger.warning("Gemini categorization failed - falling back to simple keyword matching")
        
        # Fallback to keyword matching if Gemini fails
        if any(word in cleaned_query for word in ["hello", "hi", "hey", "how are you", "what's up"]):
            return "small_talk"
        elif any(word in cleaned_query for word in ["room", "where is", "find", "location"]):
            return "room_query"
        else:
            return "faculty_query"
            
    except Exception as e:
        logger.error(f"Error during query categorization: {e}")
        return "faculty_query"  # Default to faculty query on error