from bs4 import BeautifulSoup
import requests, lxml, json

query = "Löparbilder för https://www.tjalvefriidrott.se/"

# https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
params = {
    "q": query,
    "ia": "images",
    "iax": "images",
    "first": 1
}

# https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
}

response = requests.get("https://www.duckduckgo.com", params=params, headers=headers, timeout=30)
print(response.url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())
print(soup.find_all('img'))
for index, url in enumerate(soup.find_all('img', class_='tile--img__img')):
    print(url)
    img_url = url["src"]
    image = requests.get(img_url, headers=headers, timeout=30)
    query = query.lower().replace(" ", "_")
    
    if image.status_code == 200:
        with open(f"images/tjalve_image_{index}.jpg", 'wb') as file:
            file.write(image.content)
    if index == 10:
        break