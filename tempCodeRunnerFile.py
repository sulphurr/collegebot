import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def categorize_query(query: str) -> str:
    """Uses Gemini to classify the query into 'room', 'faculty', or 'small_talk'."""
    try:
        cleaned_query = query.lower().strip()

        # Initialize Gemini model
        gemini = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.3
        )

        prompt = (
            "Classify the following query into exactly one of these categories:\n"
            "- room\n- faculty\n- small_talk\n\n"
            f"Query: '{cleaned_query}'\n\n"
            "Only return one category name from the list."
        )

        reply = gemini.invoke(prompt)
        category = reply.content.strip().lower() if reply and reply.content else None

        logger.info(f"Gemini categorization response: {category}")

        if category in {"room", "faculty", "small_talk"}:
            return category

        logger.warning(f"Unexpected Gemini response: {category}. Falling back to keyword-based classification.")

    except Exception as e:
        logger.error(f"Gemini error: {e}")

    # **Fallback keyword-based classification**
    if any(word in cleaned_query for word in ["hello", "hi", "hey", "what's up"]):
        return "small_talk"
    elif any(word in cleaned_query for word in ["room", "where is", "find", "location"]):
        return "room"
    else:
        return "faculty"
