from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

import time
import datetime
import re

def format_time(time_text):
    # Split the time_text on "." to separate day, month, and year
    parts = time_text.split(".")
    # Rearrange the parts to the desired format (year + month + day)
    formatted_time = parts[2] + parts[1].zfill(2) + parts[0].zfill(2)
    return formatted_time

def format_title(title_text):
    # Use regular expression to remove leading number and associated chars
    formatted_title = re.sub(r'^\d+[:.\s-]*', '', title_text)
    return formatted_title.strip()


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'")
    driver = webdriver.Chrome(options=options)

    subdomain = "laufen"
    base_url = "https://www.laufen.de/"

    url = f'{base_url}dlv-laufkalender'
    print("Crawling " + url)
    default_race_type = "road"

    #race_collection = RaceCollection()

    driver.get(url)
    
    data_directory = {}

    try:
        time.sleep(2)
        event_headers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "teaser.event"))
        )
        for header in event_headers:
            try:
                time_element = header.find_element(By.CLASS_NAME, 'date')
                proper_date = format_time(time_element.text)
                if not proper_date.isdigit() or len(proper_date) != 8:
                    print("Proper date is not in the format yyyymmdd")
                    continue
            except Exception as e:
                print("No time element found")
                continue
            
            try:
                title_element = header.find_element(By.CLASS_NAME, "headline.noline")
                name = format_title(title_element.text)
                print("Title:", name)
            except Exception as e:
                print("No title element found")
                continue
            # Find and print href attributes of header element
            try:
                href = f'({base_url}{header.get_attribute("href")}'
                print("Anchor Href:", href)
            except Exception as e:
                print("No anchor elements found")
            # Find and print inner text of li elements under the nav with class event-header__competitions
            competitions_nav = None
            try:
                competitions_nav = header.find_element(By.CLASS_NAME, "codes")
            except Exception as e:
                print("No competitions_nav element found")
            print("Competitions Nav:", competitions_nav)
            distances = []
            distance_str = ""
            try:
                if competitions_nav:
                    li_elements = competitions_nav.find_elements(By.CLASS_NAME, "code")
                    distances = []
                    distance_str = ""
                    for li in li_elements:
                        distance_item = li.text
                        # Convert the list to a comma-separated string
                        distance_str += f"{distance_item}, "
                        try:
                            if "KM" in distance_item or "km" in distance_item or "k" in distance_item or "K" in distance_item:
                                # Split distance_item on " " to separate potential number and distance unit
                                parts = distance_item.split()
                                #checks if first part is a number, if not it will run remaining checks
                                if parts[0].isdigit():
                                    distances.append(int(parts[0])*1000)
                                    break
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
            except Exception as e:
                print("couldnt map distances, error: {e}")
            distance_str = distance_str[:-2] #remove last comma and space
            
            #mapping from and to string in format     Strecken: 0,5 bis 14,7 Kilometer OR Strecke: 0,5 Kilometer
            try:
                from_to_distance_string_element = header.find_element(By.CLASS_NAME, "info.wettbewerbe")
                from_to_distance_string = from_to_distance_string_element.text
                print("Distance Promo Text:", from_to_distance_string)
                if "Strecke" in from_to_distance_string:
                    km_value = from_to_distance_string.split(" ")[1].replace(",", ".")
                    distance_str += f"{km_value}, "
                    distances.append(int(km_value)*1000)
                elif "Strecken" in from_to_distance_string:
                    km_value_1 = from_to_distance_string.split(" ")[1].replace(",", ".")
                    km_value_2 = from_to_distance_string.split(" ")[3].replace(",", ".")
                    distance_str += f"{km_value_1}, "
                    distance_str += f"{km_value_2}, "
                    distances.append(int(km_value_1)*1000)
                    distances.append(int(km_value_2)*1000)
            except Exception as e:
                print("No distance promo text found")
                print("Error:", e)
            
            distance_str = distance_str[:-2] #remove last comma and space
            print("Distance String:", distance_str)

            #mappig out backyard ultras
            if name.find("ackyard") != -1:
                distances = "backyard"
                race_type = "backyard"
            elif "Trail" in name or "trail" in name:
                race_type = "trail"
            else:
                race_type = default_race_type

            # Find place"
            place_element = None
            try:
                place_element = header.find_element(By.CLASS_NAME, "location")
                place = place_element.text
            except Exception as e:
                print("No competitions_nav element found")
            if place_element:
                print("Distance Promo Text:", place)
            # Populate the data_directory with data_id and inner_text
            if distance_str != "" and name is not None:
                key = f'{name}_{proper_date}'
                if key not in data_directory:
                    data_directory[key] = {
                        "name": name,
                        "proper_date": proper_date,
                        "distance_str": distance_str,
                        "distances": distances,
                        "place": place,
                        "href": href,
                        "race_type": race_type
                    } 
                if len(data_directory) > 75:
                    print("Found 75 entries, breaking loop")
                    break
        print("Finished crawling " + url)
        driver.save_screenshot("screenshot.png")
    except Exception as e:
        print("Error:", e)
    print(data_directory)
    


    # For each data_id, navigate to the detail page and check for the desired element
    for data_id in data_directory.keys():

        name = data_directory[data_id]["name"]

        print(f"---------------------Checking {name}---------------------")
        proper_date = data_directory[data_id]["proper_date"]
        race_type = data_directory[data_id]["race_type"]
        distance_str = data_directory[data_id]["distance_str"]
        distances = data_directory[data_id]["distances"]
        place = data_directory[data_id]["place"]
        detail_url = data_directory[data_id]["href"]
        driver.get(detail_url)

        # Check if the detail page contains an anchor with class "referer-link"
        website = ""
        website_ai_fallback = name
        referer_link = None
        try:
            buttons = driver.find_elements(By.CLASS_NAME, "btn")
            for button in buttons:
                if "Anmeldung" in button.text:
                    referer_link = button
                    break
        except Exception as e:
            print(f"No referer-link found for {name}")

        if referer_link:
            website_href = referer_link.get_attribute("href")
            website = website_href
            print(f"Website found for {name}: {website_href}")
        else:
            print(f"No website found for {name}")
        print("---------------------")


    # Close the browser
    driver.quit()    

if __name__ == "__main__":
    main()

