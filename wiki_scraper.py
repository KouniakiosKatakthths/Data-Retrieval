import requests
import json
import time
from bs4 import BeautifulSoup

def fetch_wikipedia(URL, depth_limit, depth = 1):
    parsed_paragraphs = {}
    print("Searching " + URL + "...")
    
    try:
        wiki_responce = requests.get(URL)
        wiki_responce.raise_for_status()        # Throw if error was encountered in the request

        # Parse the responce with BeautifulSoup
        soup_responce = BeautifulSoup(wiki_responce.text, 'html.parser')
        soup_paragraphs = soup_responce.find_all('p')

        # Remove html tags and append them to the return values if they have text
        parsed_paragraphs[URL] = [p.text.strip() for p in soup_paragraphs if p.text.strip() != ""]

        # If the maxt depth of the search has been reached exit the recursion
        if depth >= depth_limit:
            return parsed_paragraphs
        
        # Find the main content of the wiki article if exists
        body = soup_responce.find(id="mw-content-text")
        if not body:
            return parsed_paragraphs
        
        for link in body.find_all('a'):
            # If the href tag in not present or it doesn't point to an other wiki side skip it
            if not ('href' in link.attrs) or link['href'].find("/wiki/") == -1 or link['href'].find("File:") != -1:
                continue

            # Search the next wiki link
            new_paragraphs = fetch_wikipedia("https://en.wikipedia.org" + link['href'], depth_limit, depth + 1)
            # Dont spam the wiki database
            time.sleep(1)       

            # Return value is valid
            if not new_paragraphs:
                continue
            
            # Append the return values to the dictionary 
            parsed_paragraphs.update(new_paragraphs)

        return parsed_paragraphs
    except:
        print("Unable to parse link: " + URL)
        return parsed_paragraphs


#Fetch info for link with max recusive search of 2
results = fetch_wikipedia("https://en.wikipedia.org/wiki/World_War_II", 2)

filename = "wiki_scrape.json"

# Convert to json object
json_object = [
    {
        "website_url": website,
        "content": data_list, 
    }
    for website, data_list in results.items()
]

# Save as JSON file
try:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(json_object, file, indent=4)
    print(f"Data saved to JSON file: {filename}")
except IOError as e:
    print(f"Error saving to JSON file: {e}")
