from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class RemediationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert Refactoring and Security Engineer.
        Review the findings below and provide complete, refactored, production-ready code that resolves all identified issues.

        Original Code ({language}):
        ```{language}
        {code}
        ```

        Analysis & Security Findings:
        {findings}

        Output format:
        1. Explanation of fixes applied.
        2. Clean, fully refactored {language} code snippet.
        """)

    def generate_fix(self, code: str, language: str, findings: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"code": code, "language": language, "findings": findings})
        return response.content