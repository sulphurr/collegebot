#data_loader.py
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_PATH = "data/room_codes.md"


def load_documents():
    """Loads the Markdown file as a single document and cleans it."""
    loader = TextLoader(DATA_PATH, encoding="utf-8")  
    documents = loader.load()
    
    # Remove backslashes that escape characters in Markdown
    for doc in documents:
        doc.page_content = doc.page_content.replace("\\", "")
    return documents

def split_documents(documents):
    """Splits the document into chunks while preserving structure."""
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,  # Force each room to be its own chunk
    chunk_overlap=0,  # More overlap to catch related info
    separators=["\n\n", "\n", " "]  # Preserve line breaks
)

    return text_splitter.split_documents(documents)