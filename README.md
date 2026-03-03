# 📄 AI Document Assistant

A **Retrieval-Augmented Generation (RAG)** application that allows users to upload documents (PDF/DOCX) and interact with them using a **local Large Language Model (LLM)**.

Built with **LangChain** and **Gradio**, this system provides a seamless and fully private document-chat experience powered by a locally hosted LLM via Ollama.

---

## 🛠️ Prerequisites

Before running the application, ensure the following are installed:

- **Python 3.10+**
- **Ollama** – Required to run the `llama3.1` model locally
- **C++ Build Tools** – Needed to compile `chromadb` dependencies (especially on Windows)

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

Or manually place all project scripts into a single project directory.

### 2️⃣ Install Required Python Packages

```bash
pip install langchain langchain-community langchain-text-splitters \
chromadb sentence-transformers transformers torch gradio \
pypdf python-docx docx2txt langchain-ollama
```

### 3️⃣ Pull the LLM Model via Ollama

```bash
ollama pull llama3.1
```

---

## 🚀 Usage

### ▶ Run the Application

```bash
python app.py
```

### 🌐 Access the Interface

Open the local URL displayed in your terminal (typically):

```
http://127.0.0.1:7860
```

---

## 🧩 Application Workflow

### 📤 Upload
- Navigate to the **Upload** tab
- Drop a `.pdf` or `.docx` file
- Click **Process Document**

### 💬 Chat
- Go to the **Chat** tab
- Ask questions about the uploaded document
- Follow-up questions are supported

### 📄 Summarize
- Open the **Summary** tab
- Generate a concise overview of the document content

---

## 🏗️ System Architecture

### 🔹 LLM & Embeddings
- **LLM:** `llama3.1` (via Ollama)
- **Embedding Model:** `all-MiniLM-L6-v2`
- Handles reasoning and semantic retrieval

### 🔹 Vector Store
- Uses an **ephemeral (in-memory) ChromaDB instance**
- Each upload generates a **unique collection ID**
- Prevents cross-document data mixing

### 🔹 Memory Management
- Uses `ConversationBufferMemory`
- Maintains conversational context
- Clears previous states on new uploads
- Triggers manual garbage collection for privacy and performance

### 🔹 Document Splitting
- Chunk size: **1000 characters**
- Overlap: **150 characters**
- Preserves contextual continuity across chunks

---

## 📁 Project Structure

```
├── app.py
├── config.py
└── rag/
    ├── loader.py
    ├── splitter.py
    ├── embeddings.py
    ├── vectordb.py
    ├── llm.py
    └── chain.py
```

### 🔹 File Descriptions

- **app.py** – Main Gradio interface and application logic  
- **config.py** – Centralized configuration (models, paths, hyperparameters)  

Inside `rag/`:

- **loader.py** – Handles PDF and DOCX parsing  
- **splitter.py** – Manages text chunking  
- **embeddings.py** – Initializes HuggingFace embedding model  
- **vectordb.py** – Configures ChromaDB vector store  
- **llm.py** – Connects to local Ollama instance  
- **chain.py** – Builds the ConversationalRetrievalChain  

---

## 🔐 Privacy Note

All processing happens locally using Ollama and an in-memory ChromaDB instance. No document data is sent to external APIs, ensuring full privacy and data isolation.

---

## 📌 License

Ahmed Mousa Mousa Mohamed Othman.
