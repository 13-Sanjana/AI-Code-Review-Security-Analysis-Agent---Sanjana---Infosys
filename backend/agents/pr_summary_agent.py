from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class PRSummaryAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
        self.prompt = ChatPromptTemplate.from_template("""
        You are a Lead Software Architect. Generate a Pull Request (PR) Code Review Summary based on the complete multi-agent analysis report below.

        Analysis Report:
        {full_report}

        Output structured in clean Markdown:
        - ## Executive Summary
        - ## Code Health Score (out of 10)
        - ## Critical Vulnerabilities
        - ## Recommended Refactoring Steps
        - ## Deployment Approval Status (Approved / Needs Changes / Blocked)
        """)

    def summarize(self, full_report: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"full_report": full_report})
        return response.content