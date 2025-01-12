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

def MAP(results, ground_truth):
    ap_values = []
    for query, retrieved_docs in results.items():
        relevant_docs = ground_truth.get(query, [])
        ap_values.append(average_precision(retrieved_docs, relevant_docs))
    return sum(ap_values) / len(ap_values) if ap_values else 0.0