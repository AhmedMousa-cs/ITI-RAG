from langchain_ollama import OllamaLLM

def load_llm():
    return OllamaLLM(model="llama3.1")