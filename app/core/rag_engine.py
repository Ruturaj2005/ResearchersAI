import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings  # <-- NEW LIBRARY
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.llm_engine import get_llm
from dotenv import load_dotenv

load_dotenv()

# --- THE FIX: USE FASTEMBED (Local, Fast, Low RAM) ---
# This downloads a tiny model (~200MB) once and runs it on CPU.
# No API keys needed for embeddings. No Timeouts.
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def create_vector_db_from_upload(file_content: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)

        # Create Vector Store
        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(vector_store):
    llm = get_llm()
    
    # K=4 is good balance for speed/context
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    template = """You are an academic research assistant. 
    Use the following pieces of retrieved context to answer the question detailedly.
    If the answer is not in the context, say you don't know.

    Context:
    {context}

    Question: 
    {question}

    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain