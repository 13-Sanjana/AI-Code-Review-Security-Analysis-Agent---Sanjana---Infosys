import ast
import re

from models.finding import Finding
from utils.severity import get_severity


class SecurityAgent:

    def __init__(self):
        self.findings = []

    ############################################################

    def add_finding(self, rule, line, message, recommendation):

        self.findings.append(

            Finding(

                rule=rule,

                severity=get_severity(rule),

                line=line,

                message=message,

                recommendation=recommendation

            )

        )

    ############################################################

  def scan(self, code):

    self.findings = []

    # ---------- Python Analysis ----------
    try:

        tree = ast.parse(code)

        self.detect_sql_injection(tree)

        self.detect_hardcoded_secrets(tree)

        self.detect_eval_exec(tree)

        self.detect_command_injection(tree)

        self.detect_weak_crypto(tree)

        self.detect_weak_passwords(tree)

        self.detect_file_operations(tree)

    except Exception:

        pass

    # ---------- Java Analysis ----------
    self.detect_java_runtime_exec(code)

    self.detect_java_sql_injection(code)

    self.detect_java_hardcoded_secret(code)

    return self.findings
    ############################################################

    def detect_sql_injection(self, tree):

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Attribute):

                    if node.func.attr in ["execute", "executemany"]:

                        if node.args:

                            query = node.args[0]

                            if isinstance(query, ast.BinOp):

                                self.add_finding(

                                    "SQL Injection",

                                    node.lineno,

                                    "SQL query created using string concatenation.",

                                    "Use parameterized queries."

                                )

                            elif isinstance(query, ast.JoinedStr):

                                self.add_finding(

                                    "SQL Injection",

                                    node.lineno,

                                    "SQL query created using f-string.",

                                    "Use parameterized queries."

                                )
    ############################################################

    def detect_hardcoded_secrets(self, tree):

        keywords = [

            "password",

            "passwd",

            "secret",

            "token",

            "apikey",

            "api_key",

            "access_key",

            "private_key"

        ]

        for node in ast.walk(tree):

            if isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(target, ast.Name):

                        variable = target.id.lower()

                        if any(k in variable for k in keywords):

                            if isinstance(node.value, ast.Constant):

                                if isinstance(node.value.value, str):

                                    self.add_finding(

                                        "Hardcoded Secret",

                                        node.lineno,

                                        f"Hardcoded credential stored in '{target.id}'.",

                                        "Store secrets in environment variables."

                                    )
    ############################################################

    def detect_eval_exec(self, tree):

        dangerous = {

            "eval",

            "exec"

        }

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id in dangerous:

                        self.add_finding(

                            "Dangerous Function",

                            node.lineno,

                            f"Use of {node.func.id}().",

                            "Avoid eval()/exec()."

                        )
############################################################

def detect_command_injection(self, tree):

    dangerous_functions = {

        "system",
        "popen",
        "run",
        "call",
        "Popen"

    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Attribute):

                if node.func.attr in dangerous_functions:

                    self.add_finding(

                        "Command Injection",

                        node.lineno,

                        f"Dangerous command execution using {node.func.attr}().",

                        "Validate input and avoid shell=True."

                    )

            elif isinstance(node.func, ast.Name):

                if node.func.id in dangerous_functions:

                    self.add_finding(

                        "Command Injection",

                        node.lineno,

                        f"Dangerous function {node.func.id}() detected.",

                        "Avoid executing user-controlled commands."

                    )
############################################################

def detect_weak_crypto(self, tree):

    weak_algorithms = {

        "md5",

        "sha1"

    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Attribute):

                if node.func.attr.lower() in weak_algorithms:

                    self.add_finding(

                        "Weak Cryptography",

                        node.lineno,

                        f"{node.func.attr}() is insecure.",

                        "Use SHA-256 or stronger."

                    )
############################################################

def detect_weak_passwords(self, tree):

    weak_passwords = {

        "123456",

        "password",

        "admin",

        "root",

        "qwerty"

    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            if isinstance(node.value, ast.Constant):

                if isinstance(node.value.value, str):

                    if node.value.value.lower() in weak_passwords:

                        self.add_finding(

                            "Weak Password",

                            node.lineno,

                            "Weak default password detected.",

                            "Use strong randomly generated passwords."

                        )
############################################################

def detect_file_operations(self, tree):

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "open":

                    if len(node.args) >= 2:

                        mode = node.args[1]

                        if isinstance(mode, ast.Constant):

                            if mode.value == "w":

                                self.add_finding(

                                    "Insecure File Operation",

                                    node.lineno,

                                    "Opening a file in write mode without validation.",

                                    "Validate file paths before writing."

                                )
############################################################

def detect_java_runtime_exec(self, code):

    lines = code.split("\n")

    for line_no, line in enumerate(lines, start=1):

        if "Runtime.getRuntime().exec(" in line:

            self.add_finding(

                "Java Command Injection",

                line_no,

                "Runtime.exec() detected.",

                "Avoid executing OS commands directly. Use ProcessBuilder with validated input."

            )
############################################################

def detect_java_sql_injection(self, code):

    lines = code.split("\n")

    sql_keywords = [

        "SELECT",

        "INSERT",

        "UPDATE",

        "DELETE"

    ]

    for line_no, line in enumerate(lines, start=1):

        upper = line.upper()

        if any(keyword in upper for keyword in sql_keywords):

            if "+" in line:

                self.add_finding(

                    "Java SQL Injection",

                    line_no,

                    "SQL query built using string concatenation.",

                    "Use PreparedStatement with parameterized queries."

                )
############################################################

def detect_java_hardcoded_secret(self, code):

    lines = code.split("\n")

    pattern = r'.*(password|secret|token|apikey|api_key).*".+"'

    for line_no, line in enumerate(lines, start=1):

        if re.search(pattern, line, re.IGNORECASE):

            self.add_finding(

                "Hardcoded Secret",

                line_no,

                "Hardcoded credential found.",

                "Move credentials to configuration or environment variables."

            )
