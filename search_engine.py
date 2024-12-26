import json

# NLTK imports
import nltk.stem
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def request_query(query: str, index: dict) -> set:
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

# Open the save file
filepath = "inverted_index.json"
with open(filepath, "r", encoding="utf-8") as file:
    data = json.load(file)

query = input("Request query: ")
sites = request_query(query, data)

for res in sites:
    print(res) 