from pathlib import Path
from embedder import get_vectorstore

def retrieve(query, top_k=3):
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=top_k)

    sources = []
    for result, _ in results:
        metadata = result.metadata
        filename = Path(metadata.get("source", "unknown.txt")).name
        sources.append((filename, result.page_content.strip()))
    
    return sources
