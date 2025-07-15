from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

DATA_DIR = "data/docs"
INDEX_PATH = "index/faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_documents():
    docs = []
    metadata = []
    for fname in os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
            content = f.read()
            docs.append(content)
            metadata.append({"filename": fname})
    return docs, metadata

def embed_and_index():
    docs, metadata = load_documents()
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(docs)

    # FAISS index
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs(INDEX_PATH, exist_ok=True)
    faiss.write_index(index, os.path.join(INDEX_PATH, "docs.index"))

    with open(os.path.join(INDEX_PATH, "meta.pkl"), "wb") as f:
        pickle.dump(metadata, f)

if __name__ == "__main__":
    embed_and_index()
