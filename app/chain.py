from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.models import get_llm
from app.utils import model_prompt

def get_qa_chain(db):
    
    llm = get_llm()
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    prompt = PromptTemplate(template=model_prompt(), input_variables=["context", "question"])
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return qa_chain
