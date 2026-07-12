from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embedding,
    allow_dangerous_deserialization=True
)

while True:

    query = input("Ask: ")

    docs = db.similarity_search(query, k=3)

    for doc in docs:
        print(doc.page_content)
        print("-"*60)