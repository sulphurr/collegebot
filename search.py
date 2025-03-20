#search.py
import os
import google.generativeai as genai
import re
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from data_loader import load_documents, split_documents
from vector_store import process_and_store_data
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure Gemini API securely
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load and process document data
docs = load_documents()
split_docs = split_documents(docs)
vector_store = process_and_store_data(split_docs)

# Initialize Gemini model globally
MODEL = genai.GenerativeModel("models/gemini-1.5-flash")

def rephrase_with_gemini(response):
    """Rephrase the response with Gemini to make it natural, clear, and friendly but not overly enthusiastic."""
    prompt = (
        "You are a helpful and professional college room locator chatbot. "
        "Your task is to make responses natural, clear, and friendly—without sounding overly enthusiastic or exaggerated.\n\n"
        "Example of a BAD response: 'Looking for S12A? It's a great spot on the second floor of the Admin building – "
        "you'll find it right by the main stairs, with a fantastic view of the indoor basketball court!'\n"
        "Example of a GOOD response: 'Room S12A is on the second floor of the Admin block, right by the main staircase. "
        "It faces the basketball court, so it's easy to find.'\n\n"
        "Rephrase this response in a natural, clear, and slightly friendly tone:\n"
        f"{response}\n\n"
        "Keep it engaging but not too formal or overly excited."
    )

    model = genai.GenerativeModel("models/gemini-1.5-flash")

    try:
        reply = model.generate_content(prompt)
        if reply and hasattr(reply, "text"):
            return reply.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")

    return response  # Fallback to original response if Gemini fails

def search_room(query, vector_store):
    """Search for the room and return a natural response."""
    query = query.strip().upper()  # Ensure uniform case
    all_docs = vector_store.get()
    
    for doc in all_docs['documents']:
        if query in doc.upper():
            rephrased = rephrase_with_gemini(doc)
            return rephrased if rephrased else doc  # Fallback to original doc

    results = vector_store.max_marginal_relevance_search(query, k=3, fetch_k=10)
    
    if results:
        rephrased = rephrase_with_gemini(results[0].page_content)
        return rephrased if rephrased else results[0].page_content

    return "Sorry, I couldn't find that room."  # **Ensure a default return**

def get_room_info(query: str):
    """Return room information using the search engine and Gemini for rephrasing."""
    results = search_room(query, vector_store)

    if not results:
        return "Sorry, I couldn't retrieve information for your query."

    cleaned_result = results.replace("**", "").strip()

    if ": " in cleaned_result:
        cleaned_result = cleaned_result.split(": ", 1)[-1]

    if "not found" in cleaned_result.lower():
        return f"Sorry, I couldn't find a room for '{query}'. Please check the code or spelling."

    return cleaned_result
