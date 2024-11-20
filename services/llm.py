from config.config_ollama import llama

def llama3(prompt: str) -> str:
    # LLAMA 3 8B model
    return llama.invoke(prompt)

def prompt(query: str, vectors: list[str]) -> str:
    vectors_str = "\n".join(vectors)
    return llama3(f"Query: '{query}'\n\nReference Vectors:\n{vectors_str}\n\nPlease generate the output based question and reference vectors above, and provide the answer only.")