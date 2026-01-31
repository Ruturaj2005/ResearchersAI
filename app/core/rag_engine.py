from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
import tempfile
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.llm_engine import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

embeddings= HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

def create_vector_db(file_content:bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)

        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def format_docs(docs):
    """
    Helper to combine retrieved documents into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(vector_store):
    llm = get_llm()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    template = """You are an academic research assistant. 
    Use the following pieces of retrieved context to answer the question detailedly.
    If the answer is not in the context, say you don't know.

    Context:
    {context}

    Question: 
    {question}

    Answer:"""

    prompt= ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain