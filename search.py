import google.generativeai as genai
import os
import re
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def rephrase_with_gemini(response):
    """Rephrase the response with Gemini to make it more human-friendly."""
    prompt = (
        "You are a friendly room locator chatbot. Respond in concise sentences, avoid bullet point-ing. be happy and cheerful.\n"
        "Include only essential information about the room. Include minimal greetings too. Stay professional\n"
        f"Room details:\n{response}\n"
    )
    model = genai.GenerativeModel("gemini-pro")
    try:
        reply = model.generate_content(prompt)
        if reply and reply.text:
            return reply.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
    return response



def search_room(query, vector_store):
    """Search for the room and return a natural response."""
    query = query.strip().upper()  # Convert to uppercase for consistency
    all_docs = vector_store.get()
    for doc in all_docs['documents']:
        if query in doc.upper():
            return rephrase_with_gemini(doc)

    results = vector_store.max_marginal_relevance_search(query, k=2, fetch_k=10)
    return rephrase_with_gemini(results[0].page_content) if results else "Sorry, I couldn't find that room."


# Example usage
# query = "where is computer lab 1?"
# response = search_room(query, vector_store)
# print(response)
