import ast
import javalang

def validate_python(code):

    try:
        ast.parse(code)
        return True, "Python Syntax Correct"

    except SyntaxError as e:
        return False, str(e)


def validate_java(code):

    try:
        javalang.parse.parse(code)
        return True, "Java Syntax Correct"

    except javalang.parser.JavaSyntaxError as e:
        return False, str(e)

    except Exception as e:
        return False, str(e)