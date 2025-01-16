import search_engine_2
import json
import sklearn.metrics as metrics

class EvaluationValues:
    _Precision: float
    _Recall: float
    _F1_score: float
    _Map: float

    def print_values(self):
        print(f"Precission: {self._Precision}")
        print(f"Recall: {self._Recall}")
        print(f"F1 Score: {self._F1_score}")
        print(f"Map: {self._Map}")


def evaluate_query(results, ground_truth_set: set) -> EvaluationValues:
    reletive_results = []

    # Keep only reletive docs
    for link, score in results:
        if score != 0:
            reletive_results.append(link)

    y_true = [1 if link in ground_truth_set else 0 for link in reletive_results]
    y_pred = [1 if link in reletive_results else 0 for link in ground_truth_set]

    while len(y_pred) != len(y_true):
        y_pred.append(0)

    results = EvaluationValues()
    results._Precision = metrics.precision_score(y_true, y_pred)
    results._Recall = metrics.recall_score(y_true, y_pred)
    results._F1_score = metrics.f1_score(y_true, y_pred)
    results._Map = metrics.average_precision_score(y_true, y_pred)

    return results


if __name__ == "__main__":
    # Open the inverted index save file
    with open('inverted_index.json', 'r') as file:
        inverted_index = json.load(file)

    # Open the parsed data (Used for TF-IDF matrix init)
    with open('parsed_scrape.json', 'r') as file:
        parsed_scrape = json.load(file)
    
    with open('ground_truths.json', 'r') as file:
        ground_truths = json.load(file)

    print("Select Evaluation Algorithm")
    print("0. Exit")
    print("1. Boolean Retrieval")
    print("2. Vector Space Model (TF-IDF Ranking)")
    print("3. Okapi BM25")
    option = input("0,1,2,3: ")
    
    if option == "0":
        exit()
    elif option != "1" and option != "2" and option != "3":
        raise Exception(f"Invalid option: {option}")

    for index, question in enumerate(ground_truths):
        query = question['query']
        ground_truths = set(question['links'])

        result_set = search_engine_2.dataRetrival(inverted_index, parsed_scrape, option, query)

        ev = evaluate_query(result_set, ground_truths)

        print(f"\nQuery: {query}. Evaluation Values:")
        ev.print_values()

    