import re

def remove_duplicate_words_in_string(string):
    iterable = string.split()
    seen = set()
    unique_words = []
    
    for word in iterable:
        # Check if the word is not in the set (not seen before)
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    
    # Join the unique words to form the processed string
    processed_string = ' '.join(unique_words)
    
    return processed_string

def process_url(url):
   # Remove domain name endings (e.g., .com, .org)
    url = re.sub(r'\.(?![^/]*\.)[^/]+', '', url)
    print(url)
    # Remove domain name endings (e.g., .com, .org)
    url = re.sub(r'\.[a-zA-Z]+$', '', url)
    
    # Remove "https" or "http"
    url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)

    # Remove "www"
    url = re.sub('www', '', url, flags=re.IGNORECASE)

    # Replace dots with blank spaces
    url = url.replace('.', ' ')

    # Replace - with blank spaces
    url = url.replace('-', ' ')
    # Replace - with blank spaces
    url = url.replace('/', ' ')

    # Remove special characters
    url = re.sub(r'[^a-zA-Z0-9\s]', '', url)

    url = remove_duplicate_words_in_string(url)
    return url

test = process_url("https://www.tjalvefriidrott.se/tjalvefriidrott-surbulleindoorgames")
print(test)

