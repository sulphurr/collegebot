
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from vector_store import load_vector_store


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

VECTOR_DB_PATH = "./chroma_db"

_vector_store = None  

vector_store = load_vector_store()


def rephrase_with_gemini(response): #rephrase to natural tone
    prompt = (
        "You are a helpful and professional college room locator chatbot. "
        "Your task is to rewrite room descriptions in a natural, concise, and informative way while maintaining a professional tone. "
        "add a little embellishments or opinions, enough to sound engaging\n\n"
        "Example of a BAD response: 'Room S12A is awesome, on the second floor of the Admin block, facing the basketball court.'\n"
        "Example of a GOOD response: 'Room S12A is on the second floor of the Admin block, next to the main staircase. It faces the basketball court.'\n\n"
        "Here is the room description that needs rewording:\n"
        f"{response}\n\n"
        "Now, rewrite it into a clear and professional sentence:"
    )


    model = genai.GenerativeModel("models/gemini-1.5-flash")
    try:
        reply = model.generate_content(prompt)
        return reply.text.strip() if hasattr(reply, "text") else response
    except:
        return response   #gemini fails>original returns

def search_room(query, vector_store): #search room and return natural rsp
    query = query.strip().upper()
    stored_data = vector_store._collection.get(include=['documents'])
    stored_docs = stored_data['documents']
    #check direct match
    for doc in stored_docs:
        if query in doc.upper():
            return rephrase_with_gemini(doc)
    # Semantic search if no direct match
    results = vector_store.max_marginal_relevance_search(query, k=3, fetch_k=10, lambda_mult=0.5)
    if results:
        return rephrase_with_gemini(results[0].page_content)
    
    return "Sorry, I couldn't find that room."
