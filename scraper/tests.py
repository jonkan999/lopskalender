import requests
import re
from bs4 import BeautifulSoup
def get_bing_search_results(query):
    try:
        # Replace spaces with hyphens in the query
        query = query.replace(" ", "%20")

        # Bing search URL
        bing_url = f"https://www.bing.com/search?q={query}"
        print(bing_url)
        # Send a GET request to Bing
        response = requests.get(bing_url)
        
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        # Find the element with id="b_results"
        rso_element = soup.find(id='b_results')
        print(rso_element)
        # Check if the 'b_results' element exists
        if rso_element:
            # Find the first 5 child list items of 'b_results'
            child_items = rso_element.find_all('li', recursive=False)[:5]

            # Extract the first href from each child list item
            hrefs = [li.find('a')['href'] for li in child_items if li.find('a')]
            print(hrefs)
            return hrefs

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

    return None

test = get_bing_search_results("Stockholm Halvmarathon")
print(test)
