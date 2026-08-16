import ast
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class CodeAnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
        self.prompt = ChatPromptTemplate.from_template("""
        You are a Senior Software Architect. Perform a static code analysis on the following {language} code.
        Identify code smells, design anti-patterns, maintainability issues, and complexity bottlenecks.

        Code:
        ```{language}
        {code}
        ```

        Provide structured findings with clear line references and explanations.
        """)

    def analyze(self, code: str, language: str) -> str:
        # Step 1: AST Validation for Python
        ast_summary = ""
        if language.lower() == "python":
            try:
                tree = ast.parse(code)
                funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                ast_summary = f"[AST Metadata]: Found {len(classes)} class(es) and {len(funcs)} function(s).\n\n"
            except SyntaxError as e:
                return f"Syntax Error during AST parsing: {e}"

        # Step 2: LLM Quality Analysis
        chain = self.prompt | self.llm
        response = chain.invoke({"code": code, "language": language})
        return ast_summary + response.content