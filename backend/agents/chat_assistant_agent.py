from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class ChatAssistantAgent:
    def __init__(self, rag_retriever=None):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.4)
        self.rag_retriever = rag_retriever
        self.prompt = ChatPromptTemplate.from_template("""
        You are an AI Code Review Assistant. Answer the developer's question grounded in the provided code context and OWASP knowledge base.

        Code Context:
        ```{language}
        {code}
        ```

        OWASP Knowledge:
        {rag_context}

        Question: {query}
        """)

    def ask(self, query: str, code: str, language: str) -> str:
        rag_context = ""
        if self.rag_retriever:
            docs = self.rag_retriever.invoke(query)
            rag_context = "\n".join([d.page_content for d in docs])

        chain = self.prompt | self.llm
        response = chain.invoke({
            "query": query, 
            "code": code, 
            "language": language, 
            "rag_context": rag_context
        })
        return response.content