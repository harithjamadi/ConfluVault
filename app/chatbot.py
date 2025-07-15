import subprocess

def prompt_local_llm(context, question, model="mistral"):
    prompt = f"""You are a helpful assistant. Use the following documentation context to answer the user's question.

---CONTEXT START---
{context}
---CONTEXT END---

Question: {question}
Answer:"""

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()
