import json
import re       #REGEX

import nltk.stem
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def clear_special_char(text: str) -> str:
    brackets_regex = r"\[[^\]]*\]"
    alpharethmetic_regex = r"[^a-zA-Z0-9\s]"

    # Remove the references like [55] or [a]
    parsed_text = re.sub(brackets_regex, "", text)

    # The '-' many times is used as seperator to seperate the words with a ' '
    parsed_text = re.sub('-', " ", parsed_text)
    # Remove any non alapharithmetic char
    parsed_text = re.sub(alpharethmetic_regex, "", parsed_text)

    parsed_text.strip()

    return parsed_text

def preprocess_text(text: str) -> str:
    # Lemmatizer and stop word objects for english
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    # Tokenize the paragraph
    tokens = word_tokenize(text)

    # Remove all the words inside the stop word container
    non_stopwords_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Lematize the remain words
    lemmatized = [lemmatizer.lemmatize(word) for word in non_stopwords_tokens]

    # Join all the lemmatized words into a string
    final_text = " ".join(lemmatized)
    return final_text

# Open the save file
filepath = "wiki_scrape.json"
with open(filepath, "r", encoding="utf-8") as file:
    data = json.load(file)

# Parse all the text in the scrape file
parsed_data = {}
for index, site_data in enumerate(data):
    parsed_content = []
    link = site_data["website_url"]
    for p_index, paragraph in enumerate(site_data["content"]):
        # For each paragraph run clean and preprocess
        clear_paragraph = clear_special_char(paragraph)
        parsed_paragraph = preprocess_text(clear_paragraph)
        parsed_content.append(parsed_paragraph)
    
    parsed_data[link] = parsed_content

# Convert to json object
json_object = [
    {
        "website_url": website,
        "content": data_list, 
    }
    for website, data_list in parsed_data.items()
]

# Save as JSON file
filename = "parsed_scrape.json"
try:
    with open(filename, "w") as file:
        json.dump(json_object, file, indent=4)
    print(f"Data saved to JSON file: {filename}")
except IOError as e:
    print(f"Error saving to JSON file: {e}")

# Download nltk dependencies (If needed)
#nltk.download()
#nltk.download("punkt")
#nltk.download("stopwords")
#nltk.download("wordnet")

#import nltk
#try:
#    nltk.data.find('corpora/stopwords')
#    nltk.data.find('corpora/wordnet')
#except LookupError:
#    nltk.download('stopwords')
#    nltk.download('wordnet')
#    nltk.download('punkt')
