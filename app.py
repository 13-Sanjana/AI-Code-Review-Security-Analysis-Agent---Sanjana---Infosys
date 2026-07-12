from fastapi import FastAPI, UploadFile, File, Form

from validator import validate_python
from validator import validate_java
from language_detector import detect_language

app = FastAPI()


@app.get("/")
def home():
    return {"message":"AI Code Review Agent"}


@app.post("/paste")
async def paste_code(code: str = Form(...)):

    language = detect_language(code)

    if "Python" in language:
        valid, msg = validate_python(code)

    elif "Java" in language:
        valid, msg = validate_java(code)

    else:
        valid = False
        msg = "Unsupported Language"

    return {
        "language": language,
        "valid": valid,
        "message": msg
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    code = (await file.read()).decode()

    if file.filename.endswith(".py"):

        valid, msg = validate_python(code)
        language = "Python"

    elif file.filename.endswith(".java"):

        valid, msg = validate_java(code)
        language = "Java"

    else:

        return {"error":"Only Python and Java supported"}

    return {

        "filename": file.filename,
        "language": language,
        "valid": valid,
        "message": msg

    }