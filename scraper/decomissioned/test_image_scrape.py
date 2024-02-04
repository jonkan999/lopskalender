import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import unquote
from pyppeteer import launch
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def get_images_selenium(search_term):
    # Set up the Selenium WebDriver (make sure you have the appropriate driver installed)
    #setup
    options = Options()
    options.headless = True
    driver=webdriver.Chrome(options=options)
    driver.get("https://www.bing.com/images")

    # Find the search input field and send the search term
    search_box = driver.find_element("name", "q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for some time to let the page load
    time.sleep(2)
    print(driver.current_url)

    # Extract the HTML content after the search
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the first 4 image thumbnails
    thumbnails = []
    for raw_img in soup.find_all('a', class_='iusc'):
        link = raw_img.get('href')
        print(link[0:105])

        if link and link.find("&mediaurl="):
            # Find the start and end index of the substring containing img path
            start_index = link.find("&mediaurl=") + len("&mediaurl=")
            end_index = link.find("&cdnurl")
            img_url = link[start_index:end_index]

            # Decode the URL string
            decoded_img_url = unquote(img_url)
            thumbnails.append(decoded_img_url)
        if len(thumbnails) == 4:
            break

    # Close the WebDriver
    driver.quit()

    # Only return 1 to 4 as the first seems weird
    return thumbnails

async def get_images_pyp(search_term):
    # Define the Bing Images URL
    url = f"https://www.bing.com/images/search?q={search_term}&first=1"
    
    # Specify the path to the extracted Chromium
    executable_path = 'C:\\Users\\Joel\\AppData\\Local\\pyppeteer\\pyppeteer\\local-chromium\\588429\\chrome-win\\chrome.exe'

    # Launch a headless browser using pyppeteer
    browser = await launch(executablePath=executable_path)
    page = await browser.newPage()

    # Navigate to the Bing Images URL
    await page.goto(url)

    # Wait for the page to load (adjust the milliseconds as needed)
    await page.waitForTimeout(2000)

    # Get the HTML content after the page has loaded
    html_content = await page.content()

    # Close the browser
    await browser.close()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the image thumbnails
    thumbnails = []
    for raw_img in soup.find_all('a', class_='iusc'):
        link = raw_img.get('href')
        print(link[0:105])

        if link and link.find("&mediaurl="):
            # Find the start and end index of the substring containing img path
            start_index = link.find("&mediaurl=") + len("&mediaurl=")
            end_index = link.find("&cdnurl")
            img_url = link[start_index:end_index]

            # Decode the URL string
            decoded_img_url = unquote(img_url)
            thumbnails.append(decoded_img_url)
        if len(thumbnails) == 4:
            break

    # Only return 1 to 4 as the first seems weird
    return thumbnails

def get_source_images(search_term):
    # Define the Google Images URL
    url = "https://www.bing.com/images/search"
    params = {
        'q': 'Surbulle Indoor https://www.tjalvefriidrott.se/',
        'qs': 'n',
        'form': 'QBILPG',
        'sp': '-1',
        'lq': '0',
        'pq': '{search_term}',
        'sc': '0-47',
        'cvid': '9E1166B025E048E49A9CD81B9CE3AC24',
        'ghsh': '0',
        'ghacc': '0',
        'first': '1'
    }

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
    print(response.url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the 4 first image thumbnails
        thumbnails = []
        for i in range(1, 5):
          li_element = soup.find('li', {'data-idx': str(i)})
          print(li_element.innerText)
          if li_element:
              a_element = li_element.find('a')
              
              if a_element:
                link = a_element.get('href')
                print(link[0:105])
                if link and link.find("&mediaurl="):
                    # Find the start and end index of the substring containing img path
                    start_index = link.find("&mediaurl=") + len("&mediaurl=")
                    end_index = link.find("&cdnurl")
                    img_url = link[start_index:end_index]

                    # Decode the URL string
                    decoded_img_url = unquote(img_url)
                    thumbnails.append(decoded_img_url)
                if len(thumbnails) == 4:
                    break
        #Only return 1 to 4 as first seems weird
        return thumbnails
    
def get_images(search_term):
    # Define the Google Images URL
    url = "https://www.bing.com/images/search"
    params = {
        "q": search_term,
        "first": 1
    }
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    print(response.url)
    # Send a GET request to Google Images

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the 4 first image thumbnails
        thumbnails = []
        for raw_img in soup.find_all('a', class_='iusc'):
            link = raw_img.get('href')
            print(link[0:105])

            if link and link.find("&mediaurl="):
                # Find the start and end index of the substring containing img path
                start_index = link.find("&mediaurl=") + len("&mediaurl=")
                end_index = link.find("&cdnurl")
                img_url = link[start_index:end_index]

                # Decode the URL string
                decoded_img_url = unquote(img_url)
                thumbnails.append(decoded_img_url)
            if len(thumbnails) == 10:
                break

        #Only return 1 to 4 as first seems weird
        return thumbnails

    else:
        print(f"Error: {response.status_code}")
        return None
def get_image_thumbnails(search_term):
    # Define the Google Images URL
    bing_images_url = f"https://www.bing.se/images/search?q={search_term}&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&safe=active&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982"
    print(bing_images_url)
    # Send a GET request to Google Images
    response = requests.get(bing_images_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the 4 first image thumbnails
        thumbnails = []
        for raw_img in soup.find_all('img'):
          link = raw_img.get('src')
          
          if link and link.startswith("https://"):
              thumbnails.append(link)
              pass
          if len(thumbnails) == 4:
              break
        #Only return 1 to 4 as first seems weird
        return thumbnails

    else:
        print(f"Error: {response.status_code}")
        return None

def display_images(images):
    # Display images using Pillow
    for i, thumbnail in enumerate(images, 1):
        response = requests.get(thumbnail)
        img = Image.open(BytesIO(response.content))
        img.show()

# Example usage
search_term = "Löparbilder relaterade till: Surbulle Indoor https://www.tjalvefriidrott.se/"
thumbnails = get_images_selenium(search_term.replace('&', ''))
#thumbnails = asyncio.get_event_loop().run_until_complete(get_images_pyp(search_term.replace('&', '')))
print(thumbnails)
## Display the images
display_images(thumbnails)

#from bing_image_downloader import downloader
#downloader.download(search_term.replace('&', '').replace(' ', '-'), limit=10,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)




