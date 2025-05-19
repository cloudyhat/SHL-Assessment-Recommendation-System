from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "..", "data", "SHL_catalog.csv")

df = pd.read_csv(csv_path)
descriptions = [
    f"The '{row['Assessment Name']}' is a {row['Test Type']} test focused on {row['Skills']}. Duration is {row['Duration']} mins. "
    f"It supports remote testing: {row['Remote Testing Support']} and adaptive format: {row['Adaptive/IRT']}. "
    f"URL: {row['URL']}"
    for _, row in df.iterrows()
]

embedding_model = HuggingFaceEmbeddings(model_name="./local_model")
vectors = embedding_model.embed_documents(descriptions)

text_embeddings = list(zip(descriptions, vectors))

vectorstore = FAISS.from_embeddings(text_embeddings, embedding=embedding_model)

def recommend_assessments(query: str, top_k: int = 10):
    query_embedding = embedding_model.embed_query(query)
    results = vectorstore.similarity_search_by_vector(query_embedding, k=top_k)
    return results