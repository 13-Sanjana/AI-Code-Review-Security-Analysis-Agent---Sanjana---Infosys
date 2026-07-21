import ast

from models.finding import Finding
from utils.severity import get_severity


class CodeAnalysisAgent:

    def __init__(self):

        self.findings = []

    ########################################################

    def analyze(self, code):

        self.findings = []

        tree = ast.parse(code)

        self.detect_long_methods(tree)

        self.detect_large_classes(tree)

        self.detect_many_parameters(tree)

        self.detect_deep_nesting(tree)

        self.detect_unused_variables(tree)

        self.detect_complexity(tree)

        self.detect_duplicate_code(tree)

        return self.findings

    ########################################################

    def add(self, rule, line, message, recommendation):

        self.findings.append(

            Finding(

                rule=rule,

                severity=get_severity(rule),

                line=line,

                message=message,

                recommendation=recommendation

            )

        )

    ########################################################

    def detect_long_methods(self, tree):

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                statements = len(node.body)

                if statements > 20:

                    self.add(

                        "Long Method",

                        node.lineno,

                        f"{node.name} contains {statements} statements.",

                        "Split into smaller reusable methods."

                    )

    ########################################################

    def detect_large_classes(self, tree):

        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                methods = [

                    x

                    for x in node.body

                    if isinstance(x, ast.FunctionDef)

                ]

                if len(methods) > 10:

                    self.add(

                        "Large Class",

                        node.lineno,

                        f"{node.name} contains {len(methods)} methods.",

                        "Break the class into smaller classes."

                    )

    ########################################################

    def detect_many_parameters(self, tree):

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                parameters = len(node.args.args)

                if parameters > 5:

                    self.add(

                        "Too Many Parameters",

                        node.lineno,

                        f"{node.name} has {parameters} parameters.",

                        "Use objects instead of many parameters."

                    )

    ########################################################

    def detect_deep_nesting(self, tree):

        class Visitor(ast.NodeVisitor):

            def __init__(self, findings):

                self.depth = 0

                self.findings = findings

            def generic_visit(self, node):

                if isinstance(

                    node,

                    (

                        ast.If,

                        ast.For,

                        ast.While,

                        ast.Try

                    )

                ):

                    self.depth += 1

                    if self.depth > 3:

                        self.findings.append(

                            Finding(

                                "Deep Nesting",

                                get_severity("Deep Nesting"),

                                node.lineno,

                                "Nested blocks exceed level 3.",

                                "Use helper methods or early returns."

                            )

                        )

                super().generic_visit(node)

                if isinstance(

                    node,

                    (

                        ast.If,

                        ast.For,

                        ast.While,

                        ast.Try

                    )

                ):

                    self.depth -= 1

        Visitor(self.findings).visit(tree)

    ########################################################

    def detect_unused_variables(self, tree):

        assigned = {}

        used = set()

        class VariableVisitor(ast.NodeVisitor):

            def visit_Name(self, node):

                if isinstance(node.ctx, ast.Store):

                    assigned[node.id] = node.lineno

                elif isinstance(node.ctx, ast.Load):

                    used.add(node.id)

        VariableVisitor().visit(tree)

        for variable, line in assigned.items():

            if variable not in used:

                self.add(

                    "Unused Variable",

                    line,

                    f"Variable '{variable}' is never used.",

                    "Remove unused variables."

                )

    ########################################################

    def calculate_complexity(self, node):

        complexity = 1

        for child in ast.walk(node):

            if isinstance(

                child,

                (

                    ast.If,

                    ast.For,

                    ast.While,

                    ast.Try,

                    ast.BoolOp,

                    ast.ExceptHandler

                )

            ):

                complexity += 1

        return complexity

    ########################################################

    def detect_complexity(self, tree):

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                score = self.calculate_complexity(node)

                if score > 10:

                    self.add(

                        "High Cyclomatic Complexity",

                        node.lineno,

                        f"{node.name} complexity score = {score}.",

                        "Reduce branching."

                    )

    ########################################################

    def detect_duplicate_code(self, tree):

        seen = {}

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                body = ast.dump(node)

                if body in seen:

                    self.add(

                        "Duplicate Code",

                        node.lineno,

                        f"{node.name} duplicates {seen[body]}.",

                        "Extract common functionality."

                    )

                else:

                    seen[body] = node.name