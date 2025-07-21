import streamlit as st
from retriever import retrieve
from chatbot import prompt_local_llm
from pathlib import Path
from embedder import embed_and_save, INDEX_PATH

st.set_page_config(page_title="ConfluVault", page_icon="📚")
st.title("📚 ConfluVault – Ask Your Docs")

# Step 1: Ensure FAISS index file exists
index_file = INDEX_PATH / "index.faiss"
if not index_file.exists():
    with st.spinner("🔧 Embedding documents and building index..."):
        try:
            embed_and_save()
            st.success("✅ Index built successfully!")
        except Exception as e:
            st.error(f"❌ Failed to build index: {e}")
            st.stop()

# Step 2: User input
st.markdown("Ask a question based on your documents:")
query = st.text_input("🔍 Enter your question:")

# Alternative: Use st.chat_input() if you prefer modern UX (Streamlit >= 1.25)
# query = st.chat_input("Ask something...")

# Step 3: Handle query
if query:
    with st.spinner("📖 Retrieving relevant content..."):
        try:
            doc_tuples = retrieve(query)
            if not doc_tuples:
                st.warning("⚠️ No relevant documents found.")
                st.stop()
        except Exception as e:
            st.error(f"❌ Retrieval error: {e}")
            st.stop()

    with st.spinner("🧠 Generating answer with local LLM..."):
        try:
            response = prompt_local_llm(doc_tuples, query)
        except Exception as e:
            st.error(f"❌ LLM error: {e}")
            st.stop()

    # Step 4: Display results
    st.markdown("### 🧠 Answer")
    st.write(response)

    st.markdown("### 📄 Sources")
    for filename, _ in doc_tuples:
        st.markdown(f"- `{filename}`")

# Optional: File upload interface for future enhancements
# st.sidebar.header("📂 Upload new documents")
# uploaded_files = st.sidebar.file_uploader("Add Markdown or Text files", type=["md", "txt"], accept_multiple_files=True)
