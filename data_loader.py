#data_loader.py
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_PATH = "data/room_codes.md"


def load_documents(): #loads md file and cleans it ( \ and escape characters)
    loader = TextLoader(DATA_PATH, encoding="utf-8")  
    documents = loader.load()
    
    for doc in documents:
        doc.page_content = doc.page_content.replace("\\", "")
    return documents

def split_documents(documents): #splits document into chunks while maintaining structure
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,  
    separators=["\n\n", "\n", " "]  
)
    return text_splitter.split_documents(documents)
    