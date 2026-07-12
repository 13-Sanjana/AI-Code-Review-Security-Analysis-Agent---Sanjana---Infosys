from pygments.lexers import guess_lexer

def detect_language(code):

    try:
        lexer = guess_lexer(code)
        return lexer.name

    except:
        return "Unknown"