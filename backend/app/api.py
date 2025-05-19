from fastapi import FastAPI, Query
from pydantic import BaseModel
from .query import recommend_assessments

app = FastAPI()

@app.get("/")
def root():
    return {"message": "SHL Assessment Recommendation API is running. Visit /docs for usage."}

class QueryInput(BaseModel):
    query: str
    top_k: int = 10

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def recommend_endpoint(input: QueryInput):
    results = recommend_assessments(input.query, top_k=input.top_k)
    response = [{"rank": idx + 1, "content": res.page_content} for idx, res in enumerate(results)]
    return {"query": input.query, "recommendations": response}