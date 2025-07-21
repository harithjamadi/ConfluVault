## 🧰 Tech Stack

| Feature               | Tool         |
|----------------------|--------------|
| Embedding model      | sentence-transformers (MiniLM) |
| Vector store         | FAISS        |
| LLM (offline)        | Ollama + Mistral |
| UI                   | Streamlit    |
| Format support       | `.txt`, `.md`, HTML (convertible) |

---

## 🚀 Quickstart Guide

### 1️⃣ Install Python + Ollama

- Python 3.9+
- [Install Ollama](https://ollama.com/download)

---

### 2️⃣ Clone Project and Setup

```bash
git clone https://github.com/harithjamadi/ConfluVault.git
cd ConfluVault

# (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install Python dependencies
pip install -r requirements.txt
```

---

### 3️⃣ Add Your Docs

- Put your .md / .txt files in: data/docs/

---

### 4️⃣ Build the Vector Index

```bash
python app/embedder.py
```

---

### 5️⃣ Start Ollama (Local LLM)

```bash
ollama pull mistral  # One-time download
ollama run mistral
```

---

### 6️⃣ Run the Chatbot App

```bash
streamlit run app/interface.py
```
