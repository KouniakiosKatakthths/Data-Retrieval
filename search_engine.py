import nltk.stem
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""
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

"""

#β) Κατάταξη αποτελεσμάτων (Ranking)

def ranking(method_id,documents,query):

    if method_id == 1:
        #Δημιουργία TF-IDF Μήτρας
        vectorizer = TfidfVectorizer() 
        vector = vectorizer.fit_transform(documents) 
        #Μετατροπή του Query σε Διάνυσμα TF-IDF
        query_vector = vectorizer.transform([query])
        #Υπολογισμός Ομοιότητας
        scores = cosine_similarity(vector,query_vector)
        #Κατάταξη βάσει ομοιότητας και επιστροφή
        return np.argsort(scores[0])[::-1]

    return
    