import os
import shutil
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from app.models import get_embeddings

def create_vector_db(repo_path: str, db_name: str):
    
    persist_directory = f"./db_{db_name}"
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)

    allowed_extensions = {'.py', '.ipynb', '.md', '.json', '.js', '.ts', '.html', '.css', '.txt'}

    documents = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in allowed_extensions):
                file_path = os.path.join(root, file)
                try:
                    loader = TextLoader(file_path, encoding="utf-8")
                    file_docs = loader.load()
                    for d in file_docs:
                        d.metadata["source"] = file_path  
                    documents.extend(file_docs)
                except Exception:
                    pass
    if not documents:
        print("Warning: No valid documents found to process.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(texts)
    embeddings = get_embeddings()

    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def load_vector_db(db_name: str):
    persist_directory = f"./db_{db_name}"
    if not os.path.exists(persist_directory):
        return None
    
    embeddings = get_embeddings()
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vectordb