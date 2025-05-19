# SHL Assessment Recommendation System

This project is a smart web application designed to recommend relevant SHL individual assessments based on a natural language job description or query. It uses langchain, semantic search powered by vector embeddings and retrieval-augmented generation (RAG) techniques.

---

## Objective

Design and develop a system that:
1. Accepts a natural language query or job description (text or URL).
2. Recommends **up to 10 relevant SHL assessments** from SHL's product catalog.
3. Displays the recommendations in a tabular format (frontend) or JSON (API).

Each recommendation includes:
- **Assessment Name** (linked to SHL catalog URL)
- **Remote Testing Support** (Yes/No)
- **Adaptive/IRT Support** (Yes/No)
- **Duration**
- **Test Type**

---

## Approach

### 1. Data Preparation
- SHL does not provide a public API for accessing its product catalog. Attempting to programmatically extract structured data from the catalog page (https://www.shl.com/solutions/products/product-catalog/) using tools such as BeautifulSoup and requests was unsuccessful.

- So I have used a dataset which was available on the web.

### 2. Embedding & Indexing
- Used **`sentence-transformers/all-MiniLM-L6-v2`** for sentence embeddings.
- Saved locally to avoid download every time.
- Indexed all assessment descriptions using **FAISS** (Facebook AI Similarity Search).

### 3. Retrieval
- Query text is converted into an embedding.
- Retrieved the top-K most similar assessments using vector similarity search.

---