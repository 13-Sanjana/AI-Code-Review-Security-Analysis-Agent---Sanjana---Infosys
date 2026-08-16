import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class SecurityAgent:
    def __init__(self, rag_retriever=None):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
        self.rag_retriever = rag_retriever
        self.prompt = ChatPromptTemplate.from_template("""
        You are a Cybersecurity Expert. Scan the following {language} code for OWASP Top 10 vulnerabilities, hardcoded secrets, SQL injection, XSS, and unhandled security risks.

        Context from OWASP Standards:
        {owasp_context}

        Code:
        ```{language}
        {code}
        ```

        List all identified security vulnerabilities with risk level (High/Medium/Low), description, and OWASP classification.
        """)

    def scan(self, code: str, language: str) -> str:
        # Quick regex pre-scan for hardcoded secrets
        secret_patterns = [
            (r'(?i)(api_key|secret_key|password)\s*=\s*["\'][A-Za-z0-9_\-]{8,}["\']', "Potential Hardcoded Secret")
        ]
        flags = []
        for pattern, desc in secret_patterns:
            if re.search(pattern, code):
                flags.append(f"⚠️ [Static Guard] Detected {desc}")

        # RAG Context Retrieval
        owasp_context = ""
        if self.rag_retriever:
            retrieved_docs = self.rag_retriever.invoke("SQL Injection, Hardcoded Secrets, XSS, OWASP Top 10")
            owasp_context = "\n".join([doc.page_content for doc in retrieved_docs])

        chain = self.prompt | self.llm
        response = chain.invoke({
            "code": code, 
            "language": language, 
            "owasp_context": owasp_context
        })

        pre_flags = "\n".join(flags) + "\n\n" if flags else ""
        return pre_flags + response.content