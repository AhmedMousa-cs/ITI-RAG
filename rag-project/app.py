import gradio as gr
import os
import gc  # Garbage collection to force memory clear

from rag.loader import load_document
from rag.splitter import split_documents
from rag.embeddings import load_embeddings
from rag.vectordb import create_vectordb
from rag.llm import load_llm
from rag.chain import build_chain

# Global variables
vectordb = None
qa_chain = None


def process_file(file):
    global vectordb, qa_chain
    if file is None: return "Please upload a file."

    # 1. FORCE CLEAR PREVIOUS STATE
    vectordb = None
    qa_chain = None
    gc.collect()  # Manually trigger garbage collection

    # 2. LOAD NEW DATA
    docs = load_document(file.name)
    chunks = split_documents(docs)
    embeddings = load_embeddings()

    # 3. RE-INITIALIZE
    vectordb = create_vectordb(chunks, embeddings)
    llm = load_llm()
    qa_chain = build_chain(llm, vectordb)

    return f"Successfully processed: {os.path.basename(file.name)}"


def ask_question(question):
    global qa_chain
    if qa_chain is None: return "Upload a document first."

    result = qa_chain.invoke({"question": question})
    return result.get("answer", "No answer generated.")


def summarize_document():
    global vectordb
    if vectordb is None: return "Upload document first."

    # Ensure we are searching the CURRENT global vectordb
    # We use a blank query to get the most relevant chunks from the NEW file
    docs = vectordb.similarity_search(" ", k=5)

    llm = load_llm()
    from langchain.chains.summarize import load_summarize_chain

    # map_reduce is good, but 'stuff' is often more reliable for 5 chunks
    # to avoid mixing logic from previous runs
    summarize_chain = load_summarize_chain(llm, chain_type="stuff")

    result = summarize_chain.invoke({"input_documents": docs})
    return result.get("output_text", "Could not generate summary.")


# UI remains the same...
with gr.Blocks() as demo:
    gr.Markdown("# AI Document Assistant")
    with gr.Tab("Upload"):
        file_input = gr.File(file_types=[".pdf", ".docx"])
        upload_btn = gr.Button("Process Document")
        upload_output = gr.Textbox(label="Status")
        upload_btn.click(process_file, inputs=file_input, outputs=upload_output)
    with gr.Tab("Chat"):
        question_box = gr.Textbox(label="Ask anything about the file")
        ask_btn = gr.Button("Send")
        answer_box = gr.Textbox(label="Response", lines=10)
        ask_btn.click(ask_question, inputs=question_box, outputs=answer_box)
    with gr.Tab("Summary"):
        summary_btn = gr.Button("Generate Summary")
        summary_output = gr.Textbox(label="Summary", lines=15)
        summary_btn.click(summarize_document, outputs=summary_output)

demo.launch()