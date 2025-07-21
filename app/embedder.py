from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# Paths
DATA_PATH = Path("data/docs")
INDEX_PATH = Path("index/faiss_index")

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def embed_and_save():
    print(f"📁 Loading markdown files from: {DATA_PATH.resolve()}")

    # Step 1: Load all .md files
    documents = []
    for file_path in DATA_PATH.glob("**/*.md"):
        try:
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
            documents.extend(docs)
            print(f"✅ Loaded: {file_path.name} ({len(docs)} doc(s))")
        except Exception as e:
            print(f"❌ Failed to load {file_path}: {e}")

    if not documents:
        raise ValueError("No documents found to embed.")

    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = splitter.split_documents(documents)
    print(f"📝 Split into {len(texts)} chunks.")

    # Step 3: Create FAISS vector store
    db = FAISS.from_documents(texts, embedding_model)

    # Step 4: Save the index
    INDEX_PATH.mkdir(parents=True, exist_ok=True)
    db.save_local(str(INDEX_PATH))
    print(f"✅ FAISS index saved to: {INDEX_PATH.resolve()}")

    # Debug: Show saved files
    print("📦 Files in index directory:")
    for f in INDEX_PATH.glob("*"):
        print(" -", f.name)

def get_vectorstore():
    return FAISS.load_local(str(INDEX_PATH), embedding_model, allow_dangerous_deserialization=True)

# For manual run
if __name__ == "__main__":
    embed_and_save()
