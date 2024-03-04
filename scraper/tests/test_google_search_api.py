import json
from googleapiclient.discovery import build
from configuration.keys import GOOGLE_GEOCODING_API_KEY

# Import the API key from configuration/keys.py
api_key = GOOGLE_GEOCODING_API_KEY

def google_custom_search(query, api_key, cx, num_results=5, lr = "lang_no"):
    try:
        # Create a service object for interacting with the Custom Search API
        service = build("customsearch", "v1", developerKey=api_key)

        # Execute the search request
        response = service.cse().list(
            q=query, cx=cx, num=num_results, start=1, lr=lr
        ).execute()

        # Extract the URLs from the search response
        search_results = response.get("items", [])
        urls = [result.get("link") for result in search_results]

        return urls

    except Exception as e:
        print(f"An error occurred during the request: {e}")

    return None

# Define the API key and Programmable Search Engine ID (cx)
api_key = "AIzaSyAux3xaUfbq0cMaroMgM3RiLrCcuUOc0H4"  # Replace with your actual API key
cx = "34c01900926914b73"  # Replace with your actual cx ID

# Define the query
query = "Gauldalsløpet 2024"

# Perform the search
urls = google_custom_search(query, api_key, cx)

# Print the search results
if urls:
    for url in urls:
        print(url)
else:
    print("No results found.")
