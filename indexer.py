import json
from collections import defaultdict

def create_inverted_index(data):
    inverted_index = defaultdict(list)

    # For all the enties in the file
    for index, site_data in enumerate(data):
        link = site_data["website_url"]

        # For each paragraph of the entry
        for p_index, paragraph in enumerate(site_data["content"]):
            # Remove any caps
            paragraph = paragraph.lower();

            # Take only the unique words inside the paragraph
            # Split them using the ' '
            words = set(paragraph.split()) 
            
            # For every unique word in paragraph
            for word in words:
                # If the website link is not present in the on the word entry append it  
                if link not in inverted_index[word]:
                    inverted_index[word].append(link)

    return inverted_index

# Open the save file
filepath = "parsed_scrape.json"
with open(filepath, "r", encoding="utf-8") as file:
    data = json.load(file)

inverted_index = create_inverted_index(data)

# Convert to dict
inverted_index = dict(inverted_index)

# Save to JSON
index_filename = "inverted_index.json"
try:
    with open(index_filename, "w", encoding="utf-8") as file:
        json.dump(inverted_index, file, ensure_ascii=False, indent=4)
    print(f"Inverted index saved to: {index_filename}")
except IOError as e:
    print(f"Error saving inverted index: {e}")