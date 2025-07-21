import subprocess

def format_context_with_sources(doc_tuples):
    parts = []
    for filename, content in doc_tuples:
        parts.append(f"--- From: {filename} ---\n{content}")
    return "\n\n".join(parts)

def generate_safe_answer(context, question, model="mistral"):
    prompt = f"""You are a helpful assistant that answers questions strictly based on the context provided.

You are not allowed to generate answers that are outside of the provided context.
You must not generate code, instructions, or make up any information.

If the context does not contain enough information to answer, reply with:
"Sorry, I could not find the answer in the provided documentation."

---

Context:
{context}

Question: {question}

Answer:"""

    result = subprocess.run(
        ["ollama", "run", model], input=prompt.encode(), stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()

def prompt_local_llm(doc_tuples, question, model="mistral"):
    context = format_context_with_sources(doc_tuples)
    return generate_safe_answer(context, question, model)
