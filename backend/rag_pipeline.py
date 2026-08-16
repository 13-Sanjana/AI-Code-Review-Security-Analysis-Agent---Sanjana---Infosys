import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class RAGPipeline:
    def __init__(self, vectorstore_path="faiss_index"):
        self.vectorstore_path = vectorstore_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

    def build_or_load_vectorstore(self, owasp_doc_path: str = None):
        if os.path.exists(self.vectorstore_path):
            self.vectorstore = FAISS.load_local(
                self.vectorstore_path, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        elif owasp_doc_path and os.path.exists(owasp_doc_path):
            loader = PyPDFLoader(owasp_doc_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            splits = text_splitter.split_documents(docs)
            self.vectorstore = FAISS.from_documents(splits, self.embeddings)
            self.vectorstore.save_local(self.vectorstore_path)
        else:
            # Fallback mock initialization if no document is present yet
            self.vectorstore = FAISS.from_texts(
                ["OWASP Top 10 Guidelines: Secure coding practices require input validation and parameterized queries."], 
                self.embeddings
            )

    def get_retriever(():
        return self.vectorstore.as_retriever(search_kwargs={"k": 3})