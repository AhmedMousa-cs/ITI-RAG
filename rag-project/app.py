import gradio as gr
import os
import gc

from rag.loader import load_document
from rag.splitter import split_documents
from rag.embeddings import load_embeddings
from rag.vectordb import create_vectordb
from rag.llm import load_llm
from rag.chain import build_chain

# Global variables
vectordb = None
qa_chain = None
last_question = ""


def process_file(file):
    global vectordb, qa_chain
    if file is None: return "Please upload a file."

    vectordb = None
    qa_chain = None
    gc.collect()

    docs = load_document(file.name)
    chunks = split_documents(docs)
    embeddings = load_embeddings()

    vectordb = create_vectordb(chunks, embeddings)
    llm = load_llm()
    # build_chain handles internal chat history memory
    qa_chain = build_chain(llm, vectordb)

    return f"Successfully processed: {os.path.basename(file.name)}"


def chat_response(message, history):
    global qa_chain, last_question
    if qa_chain is None:
        history.append({"role": "assistant", "content": "Please upload a document first."})
        return "", history

    if not message:
        return "", history

    last_question = message
    # Invoke the chain
    result = qa_chain.invoke({"question": message})
    answer = result.get("answer", "No answer generated.")

    # Dictionary format for newer Gradio versions
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})

    return "", history


def refresh_last_response(history):
    global last_question
    if not last_question or len(history) < 2:
        return history

    # Remove last interaction (user + bot)
    history.pop()
    history.pop()

    # Re-run last question
    _, updated_history = chat_response(last_question, history)
    return updated_history


def clear_chat():
    return [], ""


def summarize_document():
    global vectordb
    if vectordb is None: return "Upload document first."

    # Search current vectordb
    docs = vectordb.similarity_search(" ", k=5)
    llm = load_llm()

    from langchain.chains.summarize import load_summarize_chain
    # 'stuff' chain type is reliable for smaller chunk counts
    summarize_chain = load_summarize_chain(llm, chain_type="stuff")
    result = summarize_chain.invoke({"input_documents": docs})

    return result.get("output_text", "Could not generate summary.")


# UI Implementation
with gr.Blocks() as demo:
    gr.Markdown("# AI Document Assistant")

    with gr.Tab("Upload"):
        file_input = gr.File(file_types=[".pdf", ".docx"])
        upload_btn = gr.Button("Process Document")
        upload_output = gr.Textbox(label="Status")
        upload_btn.click(process_file, inputs=file_input, outputs=upload_output)

    with gr.Tab("Chat"):
        chatbot = gr.Chatbot(label="Conversation History")
        question_box = gr.Textbox(label="Ask anything about the file")

        with gr.Row():
            ask_btn = gr.Button("Send", variant="primary")
            refresh_btn = gr.Button("Refresh Last Response")
            clear_btn = gr.Button("Clear Chat")

        ask_btn.click(chat_response, [question_box, chatbot], [question_box, chatbot])
        question_box.submit(chat_response, [question_box, chatbot], [question_box, chatbot])

        refresh_btn.click(refresh_last_response, [chatbot], [chatbot])
        clear_btn.click(clear_chat, outputs=[chatbot, question_box])

    with gr.Tab("Summary"):
        summary_btn = gr.Button("Generate Summary")
        summary_output = gr.Textbox(label="Summary", lines=15)
        # Fixed the NameError by ensuring this function exists above
        summary_btn.click(summarize_document, outputs=summary_output)

demo.launch()