from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from scraper_package.race_classes import Race, RaceCollection
import time
import datetime
import re

def remove_years_and_spaces(input_string):
    # Define a regular expression pattern to match any of the strings "2023" through "2040"
    # and any space that might be present before them
    pattern = r'(\s|^)(2023|2024|2025|2026|2027|2028|2029|2030|2031|2032|2033|2034|2035|2036|2037|2038|2039|2040)'
    
    # Use the re.sub() function to replace any matched strings with an empty string
    result = re.sub(pattern, '', input_string)
    
    return result

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'")
    driver = webdriver.Chrome(options=options)

    subdomain = "friidrett"

    today = '20'+datetime.date.today().strftime("%y-%m-%d")
    base_url = "https://live.eqtiming.com"
    url = f"{base_url}/?fullscreen=true&scroll=true&sportIds=19&organizationId=17&theme=nfif&showlevel=false&validated=true&locale=no&minDate={today}#eventlist"
    default_race_type = "road"

    race_collection = RaceCollection()

    driver.get(url)
    
    # Wait for JavaScript to load and possibly generate the button
    wait = WebDriverWait(driver, 5)  # Maximum wait time is 5 seconds
    # Wait for the first item with the class 'eventlist-container-item' to appear
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "eventlist-container-item"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    data_directory = {}

    for item in soup.find_all(class_="eventlist-container-item"):
        # Get the data-id attribute value
        data_id = item.get("data-id")

        # Find the element with class eventlist-container-item-description
        description = item.find(class_="eventlist-container-item-description")

        # Find the h3 element inside the a child of the description element
        if description:
            h3 = description.find("a").find("h3")

            # Extract the inner text of the h3 element
            if h3 is not None:
                name = h3.get_text(strip=True)
            else:
                name = None

        proper_date = item.get("data-date").replace("-", "")
        print(f"Data ID: {data_id}, Name: {name}, Proper Date: {proper_date}")
        

        #check if race exists in collection, otherwise continue
        current_races = RaceCollection()
        if current_races.exists_in_source(name, proper_date, base_url):
            print(f'{name} already exists in source, continue')
            continue

        # Populate the data_directory with data_id and inner_text
        if data_id is not None and name is not None:
            data_directory[data_id] = {"name": name, "proper_date": proper_date}

    print(data_directory)

    # Navigate to the main page
    driver.get("https://live.eqtiming.com")

    # For each data_id, navigate to the detail page and check for the desired element
    for data_id in data_directory.keys():

        remove_years_and_spaces(data_directory[data_id]["name"])
        name = data_directory[data_id]["name"]

        print(f"---------------------Checking {name}---------------------")
        proper_date = data_directory[data_id]["proper_date"]
        detail_url = f"https://live.eqtiming.com/{data_id}#eventinfo"
        driver.get(detail_url)
        # Use a WebDriverWait to wait for the detail page to load
        try:
            detail_row_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "detail-list-row"))
            )
        except:
            print(f"Element not found, aborting and continuing from the next iteration")
            continue

        website = ""
        website_ai_fallback = name
        place = None
        organizer = None
        try:
            for element in detail_row_elements:
                try:
                    #print(f"Checking {element.get_attribute('outerHTML')}")
                    # Find the span element
                    span_element = element.find_element(By.XPATH, ".//span")
                    text = span_element.text

                    if text == "Webpage:":
                        try:
                            # Find the a element inside the span element
                            webpage_element = element.find_element(By.XPATH, ".//a")
                            # Get the href attribute
                            website = webpage_element.get_attribute("href")
                            if website == "http:// " or website == "https:// " or website == "http://":
                                print(f"No Webpage URL found for {data_id}")
                                website = ""
                            print(f"Webpage URL for {data_id}: {website}")
                        except:
                            print(f"No Webpage URL found for {data_id}")
                            website = ""

                    if text == "Sted:":
                        place = element.find_elements(By.CLASS_NAME, "text")[0].text
                        print(f"Place for {data_id}: {place}")

                    if text == "Arrangør:":
                        organizer = element.find_elements(By.CLASS_NAME, "text")[0].text
                        print(f"organizer for {data_id}: {place}")
                except:
                    print(f"error searching for info for {data_id}")

        except TimeoutException:
            # If the timeout is reached, print a message
            print(f"error searching for info for {data_id}")

        # Find the element with class 'row eventinfo
        try:
            
            race_info_box = driver.find_element(By.CLASS_NAME, "row.eventinfo-race")
        except:
            print(f"Element not found, aborting and continuing from the next iteration")
            continue

        # Find the elements with class 'row' inside the race_element
        try:
            distance_elements_rows = race_info_box.find_elements(By.CLASS_NAME, "row")
            distance_elements = []
            for row in distance_elements_rows:
                div_elements = row.find_elements(By.TAG_NAME, "div")
                distance_elements.extend(div_elements)
        except:
            print("Error finding distance elements")
            continue
        
        # Iterate through the row_elements and get the text in their h3 elements
        distances = []
        distance_str = ""
        for row in distance_elements:
            h3_element = row.find_element(By.TAG_NAME, "h3")
            distance_item = h3_element.text
            # Convert the list to a comma-separated string
            distance_str += f"{distance_item}, "
            #print(f"Text in h3 element: {text}")
            #mapping distances to meters
            try:
                if "KM" in distance_item or "km" in distance_item or "k" in distance_item or "K" in distance_item:
                    # Split distance_item on " " to separate potential number and distance unit
                    parts = distance_item.split()
                    for i in range(len(parts)):
                        part = parts[i]
                        if "," in part or "." in part:
                            distance_item = distance_item.split(",")[0] #get first digit if fraction
                            distances.append(int(distance_item)*1000)
                            break #should not break here, this will cause the loop to only run once when it finds decimals but it should run for all elements
                        elif part[-1] in ['k', 'K', 'm', 'M']:
                            # Extract the number and multiply it by 1000
                            reduced_part = part[:-1].replace(",", "").replace(".", "").replace("km", "").replace("KM", "").replace("K", "").replace("k", "")
                            reduced_parts = parts[i-1].replace(",", "").replace(".", "").replace("km", "").replace("KM", "").replace("K", "").replace("k", "")
                            if reduced_part.isdigit():
                                distances.append(int(float(reduced_part)*1000))
                            elif reduced_parts.isdigit():
                                distances.append(int(float(reduced_parts)*1000))
                elif distance_item in ["Halvmaraton", "Half Marathon"]:
                    distances.append(21097)
                elif distance_item in ["Maraton", "Marathon"]:
                    distances.append(42195)
                elif "MILES" in distance_item:
                    try:
                        for match in re.findall(r"(\d+)\s*KM", distance_item):
                            distances.append(int(match)*1609)
                    except:
                        pass
                else:
                    try:
                        distances.append(int(distance_item)*1000)
                    except:
                        pass
            except:
                print(f"Error parsing distance {distance_item}")

                # for terrain races continue if we dont get any distances
        if len(distances) == 0:
            print(f"Error parsing distance for {data_id}")
            continue

        distance_str = distance_str[:-2] #remove last comma and space
        print("---------------------")
        print(f"date = {proper_date}, type = {default_race_type}, name = {name}, distance = {distance_str}, distance_m = {distances}, place = {place}, organizer = {organizer}, website = {website}, src_url = {url}, website_ai_fallback = {website_ai_fallback}")
        race = Race(date = proper_date, type =  default_race_type,  name = name, distance = distance_str, distance_m = distances, place = place, organizer = organizer, website = website, src_url = base_url, website_ai_fallback = website_ai_fallback)
        # Check if race already exists but on other distance
        appended = False
        for prev_race in race_collection.races:
            if prev_race['date'] == proper_date and prev_race['name'] == name and prev_race['src_url'] == url:
                prev_race['distance_m'].extend(distances)
                prev_race['distance_m'].sort()
                appended = True
            elif prev_race['date'] == proper_date and (prev_race.similar_race_ratio(name) > 0.5):
                prev_race['distance_m'].extend(distances)
                prev_race['distance_m'].sort()
                appended = True
        if not appended:
            ### STANDARD ENDING ###
            race.add_id('extract')
            race_collection.add_race_if_doesnt_exist('extraction/sourced_races.json', race)

    race_collection.append_or_create_source_json(subdomain)
    race_collection.append_or_create_source_json()
    print("Finished crawling " + url)

    # Close the browser
    driver.quit()
if __name__ == "__main__":
    main()

