from query import recommend_assessments

# Example benchmark set
benchmark = [
    {
        "query": "Looking for Java developer with remote testing and 40 mins duration",
        "relevant": ["Java Developer Assessment #1", "Java Coding Drill #47"]
    },
    {
        "query": "Teamwork and communication assessment under 40 mins",
        "relevant": ["Collaboration Skills Evaluation #28"]
    }
]

def recall_at_k(relevant, retrieved, k):
    retrieved_at_k = retrieved[:k]
    hits = len([r for r in retrieved_at_k if r in relevant])
    return hits / len(relevant)

def apk(relevant, retrieved, k):
    score = 0.0
    hits = 0
    for i, r in enumerate(retrieved[:k]):
        if r in relevant and r not in retrieved[:i]:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(relevant), k)

def evaluate(benchmark, k=3):
    total_recall = 0
    total_map = 0
    for item in benchmark:
        query = item["query"]
        relevant = item["relevant"]
        results = recommend_assessments(query, top_k=k)
        predicted_names = [res.page_content.split("'")[1] for res in results]

        recall = recall_at_k(relevant, predicted_names, k)
        ap = apk(relevant, predicted_names, k)

        total_recall += recall
        total_map += ap

    mean_recall = total_recall / len(benchmark)
    mean_ap = total_map / len(benchmark)

    print(f"Mean Recall@{k}: {mean_recall:.3f}")
    print(f"MAP@{k}: {mean_ap:.3f}")

if __name__ == "__main__":
    evaluate(benchmark, k=3)