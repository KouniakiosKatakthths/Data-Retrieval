import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def boolean_retrieval(query: str, index: dict) -> set:
    logic_operators = {"and", "or", "not"};

    # Init nltk objects
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english')) - logic_operators

    # Tokenize query
    tokens = word_tokenize(query.lower())

    # Remove all the stop words inside the query tokens
    non_stopwords_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Lematize the remain words
    lemmatized_query = [lemmatizer.lemmatize(word) for word in non_stopwords_tokens];

    # Remove any duplicates
    result = set()

    # Default search op is logic or
    op = "or"

    for token in lemmatized_query:
        # Chnage mode
        if token.lower() in logic_operators:
            op = token.lower()
            continue

        # Token is not found
        if token not in index:
            continue
        
        url_list = set(index[token])

        # Sets allow logic operations on 
        if op == "or":
            result |= url_list  # If or join the two url lists
        elif op == "and":
            result &= url_list  # If and take the common links only
        elif op == "not":
            result -= url_list  # If not remove the links from the result

    return result

def ranking_TF_IDF(result_set: set, parsed_scrape: dict):
    # Combine the URL and the paragraphs in a signle line
    documents = {entry['website_url']: " ".join(entry['content']) for entry in parsed_scrape}
    
    # Remove documents that arent in the result set
    documents = {url: content for url, content in documents.items() if url in result_set}

    # Init the TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents.values())

    # The results of the search in TF-IDF 
    result_vector = vectorizer.transform([" ".join(result_set)])

    scores = cosine_similarity(result_vector, tfidf_matrix).flatten()
    ranked_results = sorted(zip(documents.keys(), scores), key=lambda x: x[1], reverse=True)

    return ranked_results


if __name__ == "__main__":
    # Open the inverted index save file
    inverted_index_filepath = "inverted_index.json"
    with open(inverted_index_filepath, "r", encoding="utf-8") as file:
        inverted_index = json.load(file)

    parsed_scrape_filepath = "parsed_scrape.json"
    with open(parsed_scrape_filepath, "r", encoding="utf-8") as file:
        parsed_scrape = json.load(file)

    query = input("Request query: ")
    result_set = boolean_retrieval(query, inverted_index)

    ranked_results = ranking_TF_IDF(result_set, parsed_scrape)

    for score, url in ranked_results:
        print(f"Score: {score}. For URL: {url}")