from langchain_community.vectorstores import Chroma
from config import DB_DIR
import chromadb
import uuid


def create_vectordb(chunks, embeddings):
    # Use a unique name for every upload so data never mixes
    unique_collection_name = f"col_{uuid.uuid4().hex}"

    # Create a strictly in-memory client
    client = chromadb.EphemeralClient()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        client=client,
        collection_name=unique_collection_name
    )
    return vectordb