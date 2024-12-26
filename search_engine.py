import nltk.stem
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def request_query(query: str, index: dict) -> set:
    # Init nltk objects
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # Tokenize query
    tokens = word_tokenize(query.lower())

    # Remove all the stop words inside the query tokens
    non_stopwords_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Lematize the remain words
    lemmatized = [lemmatizer.lemmatize(word) for word in non_stopwords_tokens]

    result = set()
    op = "or"

    for token in lemmatized_query:
        if token.lower() in { "and", "or", "not" }:
            op = token.lower()
    

    return result

print("\n=== Avaiable Retrieval Algorithms ===")
print("1 -> Boolean Retrieval")
print("2 -> Vector Space Model (VSM)")
print("3 -> Probabilisic Retrieval Models (Okapi BM25)")
algorithm = input("Select retrieval algorithn (1/2/3): ")
while (algorithm != '1' and algorithm != '2' and algorithm != '3'):
    algorithm = input("Invalid option. Select retrieval algorithn (1/2/3): ")

