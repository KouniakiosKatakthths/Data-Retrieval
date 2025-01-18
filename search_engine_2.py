import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from rank_bm25 import BM25Okapi

logic_operators = {"and", "or", "not"}

def preprocess_query(query: str, exclude_words: set = set()) -> str:

    # Init nltk objects
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english')) - exclude_words

    # Tokenize query
    tokens = word_tokenize(query.lower())
    # Remove all the stop words inside the query tokens
    non_stopwords_tokens = [word for word in tokens if word.lower() not in stop_words]
    # Lematize the remain words
    lemmatized_query = " ".join([lemmatizer.lemmatize(word) for word in non_stopwords_tokens])

    return lemmatized_query

def ranking_TF_IDF(parsed_scrape: dict, query: str, result_set: set = None):

    if not query:
        return {}

    # Preprocess the query
    lemmatized_query = preprocess_query(query, logic_operators)

    # Combine the URL and the paragraphs in a signle line
    documents = {entry['website_url']: " ".join(entry['content']) for entry in parsed_scrape}
    
    # A Result set has been provided
    if result_set is not None:

        # Remove documents that arent in the result set
        documents = {url: content for url, content in documents.items() if url in result_set}

    # Init the TF-IDF matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents.values())

    query_vector = vectorizer.transform([lemmatized_query])

    scores = cosine_similarity(query_vector, tfidf_matrix).flatten()  # Using flatter to conv to vectoer
    ranked_results = sorted(zip(documents.keys(), scores), key=lambda x: x[1], reverse=True)

    return ranked_results
    
def boolean_retrieval(query: str, index: dict) -> set:
    
    if not query: 
        return {}
    
    # Preprossess query to remove any unwanted words or characters, keeping the logic ops
    lemmatized_query = preprocess_query(query, logic_operators)

    # Remove any duplicates
    result = set()

    # Default search op is logic or
    op = "or"

    for token in lemmatized_query.split():
        # Chnage mode
        if token.lower() in logic_operators:
            op = token.lower()
            continue

        # Token is not found
        if token not in index:
            continue
        
        url_list = set(index[token])

        # Sets allow logic operations on pyth
        if op == "or":
            result |= url_list  # If or join the two url lists
        elif op == "and":
            result &= url_list  # If and take the common links only
        elif op == "not":
            result -= url_list  # If not remove the links from the result

    return result

def vsm_retrieval(query: str, parsed_scrape: dict):
    if not query:
        return {}

    processed_query = preprocess_query(query)

    results = ranking_TF_IDF(parsed_scrape, processed_query)
    return results

def probabilistic_retrieval(parsed_scrape: list, query: str):
    if not query:
        return []

    # Preprocess the query
    processed_query = preprocess_query(query)

    # Combine the URL and the paragraphs in a signle line
    documents = {entry['website_url']: " ".join(entry['content']) for entry in parsed_scrape}

    # Tokenize documents
    tokenized_documents = [word_tokenize(doc.lower()) for doc in documents.values()]

    # Initialize BM25 model
    bm25 = BM25Okapi(tokenized_documents)

    # Tokenize the query
    tokenized_query = word_tokenize(processed_query)

    # Get BM25 scores
    scores = bm25.get_scores(tokenized_query)
    ranked_results = sorted(zip(documents.keys(),scores), key=lambda x: x[1], reverse=True)

    return ranked_results

def dataRetrival(inverted_index: dict, parsed_scrape: dict, option: str, query: str) -> set:
    result_set = set()
    if option == "1":
        bool_results = boolean_retrieval(query, inverted_index)
        result_set = ranking_TF_IDF(parsed_scrape, query, bool_results)
    elif option == "2":
        result_set = vsm_retrieval(query, parsed_scrape)
    elif option == "3":
        result_set = probabilistic_retrieval(parsed_scrape,query)
    else:
        raise Exception(f"Invalid Retrival Method: \"{option}\"")
    
    return result_set

if __name__ == "__main__":
    # Open the inverted index save file
    with open('inverted_index.json', 'r') as file:
        inverted_index = json.load(file)

    # Open the parsed data (Used for TF-IDF matrix init)
    with open('parsed_scrape.json', 'r') as file:
        parsed_scrape = json.load(file)

    print("Options:")
    print("0. Exit")
    print("1. Boolean Retrieval")
    print("2. Vector Space Model (TF-IDF Ranking)")
    print("3. Okapi BM25")
    option = input("0,1,2,3: ")
    if option == "0":
        exit()

    query = input("Request query: ")

    result_set = dataRetrival(inverted_index, parsed_scrape, option, query)

    print("\nResults: ")
    for score, url in result_set:
        print(f"URL: {score}. Score: {url}")
