# 📄 AI Document Assistant – Project Summary

## 🔎 Overview

The **AI Document Assistant** is a Retrieval-Augmented Generation (RAG) system that enables users to upload PDF or DOCX documents and interact with them through a conversational interface powered by a local Large Language Model (LLM).

The system ensures privacy by running entirely on the user's machine using Ollama and an in-memory vector database.

---

## 🎯 Objectives

- Enable intelligent document-based question answering
- Provide contextual follow-up conversations
- Generate concise document summaries
- Maintain full local privacy without external API calls

---

## 🏗️ Technical Stack

### 🔹 Core Framework
- LangChain – Orchestrates the RAG pipeline

### 🔹 Large Language Model
- llama3.1 (via Ollama) – Handles reasoning and response generation

### 🔹 Embedding Model
- all-MiniLM-L6-v2 – Converts document chunks into vector embeddings

### 🔹 Vector Database
- ChromaDB (Ephemeral/In-Memory) – Stores embeddings temporarily per session

### 🔹 User Interface
- Gradio – Provides a multi-tab web interface (Upload, Chat, Summary)

---

## ⚙️ System Workflow

1. Document Upload
   - User uploads a PDF or DOCX file
   - The system parses and extracts text

2. Text Chunking
   - Text is split into 1000-character chunks
   - 150-character overlap preserves contextual continuity

3. Embedding Generation
   - Each chunk is converted into a vector representation

4. Vector Storage
   - Embeddings are stored in a unique in-memory ChromaDB collection

5. Conversational Retrieval
   - User queries are embedded
   - Relevant chunks are retrieved
   - LLM generates context-aware responses

6. Summarization
   - Uses LangChain's summarize chain ("stuff" type)
   - Produces concise document overviews

---

## 🧠 Key Features

- Conversational memory using ConversationBufferMemory
- Manual state clearing between uploads
- Explicit garbage collection for clean sessions
- Session-isolated vector collections
- Fully local and private processing

---

## 🔐 Privacy & Data Handling

All data processing occurs locally:

- No external API calls
- No cloud storage
- No document persistence after session reset

This ensures complete data isolation and user privacy.

---

## 📌 Conclusion

The AI Document Assistant demonstrates a clean and modular implementation of a RAG pipeline using LangChain, ChromaDB, and a locally hosted LLM. It combines document understanding, semantic retrieval, and conversational AI into a lightweight, privacy-focused application suitable for research, productivity, and educational use cases.