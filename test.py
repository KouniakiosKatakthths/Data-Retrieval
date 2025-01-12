import search_engine_2
import json

def precision(retrieved, relevant):
    if not retrieved:
        return 0.0
    return len(set(retrieved) & set(relevant)) / len(retrieved)

def recall(retrieved, relevant):
    if not relevant:
        return 0.0
    return len(set(retrieved) & set(relevant)) / len(relevant)

def f1_score(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def average_precision(retrieved, relevant):
    if not relevant:
        return 0.0

    precisions = []
    num_relevant = 0

    for i, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            num_relevant += 1
            precisions.append(num_relevant / i)

    return sum(precisions) / len(relevant) if precisions else 0.0

def MAP(results, ground_truth) -> float:
    ap_values = []
    for query, retrieved_docs in results.items():
        relevant_docs = ground_truth.get(query, [])
        ap_values.append(average_precision(retrieved_docs, relevant_docs))
    return sum(ap_values) / len(ap_values) if ap_values else 0.0

if __name__ == "__main__":
    # Open the inverted index save file
    with open('inverted_index.json', 'r') as file:
        inverted_index = json.load(file)

    # Open the parsed data (Used for TF-IDF matrix init)
    with open('parsed_scrape.json', 'r') as file:
        parsed_scrape = json.load(file)

    