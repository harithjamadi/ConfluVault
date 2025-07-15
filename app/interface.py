import streamlit as st
from retriever import retrieve
from chatbot import prompt_local_llm

st.title("📚 Internal Docs Chatbot (Offline)")
query = st.text_input("Ask a question about your docs:")

if query:
    with st.spinner("Searching documents..."):
        docs = retrieve(query)
        context = "\n\n".join(docs)

    with st.spinner("Thinking..."):
        response = prompt_local_llm(context, query)

    st.markdown("### 🧠 Answer")
    st.write(response)
