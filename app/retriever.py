from sentence_transformers import SentenceTransformer
import faiss
import pickle

INDEX_PATH = "index/faiss_index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def retrieve(query, top_k=5):
    index = faiss.read_index(f"{INDEX_PATH}/docs.index")
    with open(f"{INDEX_PATH}/meta.pkl", "rb") as f:
        metadata = pickle.load(f)

    model = SentenceTransformer(MODEL_NAME)
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, top_k)

    results = []
    for i in indices[0]:
        with open(f"data/docs/{metadata[i]['filename']}", "r", encoding="utf-8") as f:
            results.append(f.read())
    return results
