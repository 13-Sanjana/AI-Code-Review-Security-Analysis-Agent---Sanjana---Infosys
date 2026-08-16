from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional

from rag_pipeline import RAGPipeline
from agents.code_analysis_agent import CodeAnalysisAgent
from agents.security_agent import SecurityAgent
from agents.remediation_agent import RemediationAgent
from agents.pr_summary_agent import PRSummaryAgent
from agents.chat_assistant_agent import ChatAssistantAgent

app = FastAPI(title="AI Code Reviewer & Security Analysis API", version="1.0")

# Initialize RAG Pipeline and Agents
rag = RAGPipeline()
rag.build_or_load_vectorstore()
retriever = rag.get_retriever()

code_agent = CodeAnalysisAgent()
security_agent = SecurityAgent(rag_retriever=retriever)
remediation_agent = RemediationAgent()
pr_agent = PRSummaryAgent()
chat_agent = ChatAssistantAgent(rag_retriever=retriever)

class CodeReviewRequest(BaseModel):
    code: str
    language: str

class ChatRequest(BaseModel):
    query: str
    code: str
    language: str

@app.post("/api/review")
async def full_review(req: CodeReviewRequest):
    code = req.code
    lang = req.language

    # Step 1: Code Analysis
    analysis_res = code_agent.analyze(code, lang)
    
    # Step 2: Security Scan
    security_res = security_agent.scan(code, lang)
    
    # Combined Findings
    combined_findings = f"### Code Quality Analysis\n{analysis_res}\n\n### Security Audit\n{security_res}"
    
    # Step 3: Remediation Generation
    remediation_res = remediation_agent.generate_fix(code, lang, combined_findings)
    
    # Step 4: PR Summary
    full_report = f"{combined_findings}\n\n### Proposed Fixes\n{remediation_res}"
    pr_summary = pr_agent.summarize(full_report)

    return {
        "analysis": analysis_res,
        "security": security_res,
        "remediation": remediation_res,
        "pr_summary": pr_summary
    }

@app.post("/api/chat")
async def chat_with_assistant(req: ChatRequest):
    answer = chat_agent.ask(req.query, req.code, req.language)
    return {"reply": answer}