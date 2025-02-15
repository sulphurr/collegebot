from data_loader import load_documents, split_documents
from vector_store import process_and_store_data

# Step 1: Load documents
docs = load_documents()

# Step 2: Split documents into chunks
split_docs = split_documents(docs)

# Step 3: Rebuild vector store
vector_store = process_and_store_data(split_docs)
print("Vector store updated with new markdown content.")
