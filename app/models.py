import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

def get_embeddings():
    
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))

def get_llm():
    
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, top_p=0.85, google_api_key=os.getenv("GOOGLE_API_KEY"))