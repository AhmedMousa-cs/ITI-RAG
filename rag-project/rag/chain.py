# rag/chain.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import RETRIEVER_K

def build_chain(llm, vectordb):
    # الذاكرة داخل الدالة لضمان عدم حدوث Error عند تغيير الملفات
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": RETRIEVER_K}
    )

    # بناء الـ Chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True
    )

    return qa_chain