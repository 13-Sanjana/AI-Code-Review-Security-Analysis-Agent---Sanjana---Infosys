import streamlit as st
import requests

st.title("AI Code Review Agent")

option = st.radio(
    "Choose",
    ["Paste Code","Upload File"]
)

if option=="Paste Code":

    code = st.text_area("Paste your code")

    if st.button("Submit"):

        response = requests.post(
            "http://127.0.0.1:8000/paste",
            data={"code":code}
        )

        st.json(response.json())


else:

    file = st.file_uploader(
        "Upload File",
        type=["py","java"]
    )

    if file:

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files={"file":file}
        )

        st.json(response.json())