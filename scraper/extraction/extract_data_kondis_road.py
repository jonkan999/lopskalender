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
import re

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'")
    driver = webdriver.Chrome(options=options)

    subdomain = "kondis"
    base_url = "https://terminlista.kondis.no/l%C3%B8ping?underlag=asfalt&pagesize=200&page={}"
    default_race_type = "road"

    race_collection = RaceCollection()

    for page_number in range(1, 11):  # Iterate over pages 1 to 10
        url = base_url.format(page_number)
        driver.get(url)

        # Check if the page exists
        if "Fant ingen arrangementer" in driver.page_source:
            print(f"No more pages found after page {page_number - 1}. Quitting.")
            break

        # Wait for JavaScript to load and possibly generate the button
        wait = WebDriverWait(driver, 5)  # Maximum wait time is 5 seconds

        try:
            # Locate the parent element with the class "qc-cmp2-summary-buttons"
            parent_element_selector = ".qc-cmp2-summary-buttons"
            parent_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, parent_element_selector)))

            # Locate the second child button element
            button_selector = f"{parent_element_selector} > :nth-child(2)"
            button_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, button_selector)))

            # Click the button
            button_element.click()

            # Get the updated page source after JavaScript execution
            html_content = driver.page_source

            # Now you can continue with other actions or data extraction
            # ...

        except TimeoutException:
            print("Button not found within 5 seconds. Proceeding without clicking.")
            html_content = driver.page_source

        # Now you can use BeautifulSoup on the updated HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the main table with class 'mat-table cdk-table mat-sort'
        main_element = soup.find(class_="mat-table")

        if main_element:
            # Find the tbody child of the main table
            tbody = main_element.find("tbody")
            if tbody:
                # Iterate through each row (tr) in the tbody
                for row in tbody.find_all("tr"):
                    if row.find("img", alt="Kvalitetsløp") is None:
                        continue  # Skip this row if the image is not found

                    # Extract date_text, name, place, and distance_str as before
                    date_text = row.select_one("td.mat-cell.cdk-cell.col-3.col-sm-2.d-flex.align-items-center.cdk-column-date.mat-column-date.ng-star-inserted > span.date.d-none.d-md-block").text.strip()
                    day, month_name, year = date_text.split(" ")[0], date_text.split(" ")[1], date_text.split(" ")[2]

                    # Dictionary to map month names to month numbers
                    months_dict = {
                        "jan": "01",
                        "feb": "02",
                        "mar": "03",
                        "apr": "04",
                        "mai": "05",
                        "jun": "06",
                        "jul": "07",
                        "aug": "08",
                        "sep": "09",
                        "okt": "10",
                        "nov": "11",
                        "des": "12"
                    }

                    # Extract the first three characters of the month name in lowercase
                    short_month_name = month_name[:3].lower()

                    # Get the corresponding month number from the dictionary
                    month_num = months_dict.get(short_month_name, "00")

                    # Create the proper_date string
                    proper_date = f"{year}{month_num}{day}"
                    name = row.select_one("td.mat-cell.cdk-cell.col-8.col-sm-6.col-md-4.col-lg-3.d-flex.align-items-center.cdk-column-name.mat-column-name.ng-star-inserted > a").text.strip()
                    print(name)
                    place = row.select_one("td.mat-cell.cdk-cell.col-3.col-md-2.d-none.d-sm-flex.align-items-center.cdk-column-location.mat-column-location.ng-star-inserted > span").text.strip()
                    distance_str = ""
                    distances = []
                    try:
                        distance_str = row.select_one("td.mat-cell.cdk-cell.col-md-2.col-lg-3.d-none.d-md-flex.align-items-center.cdk-column-distances.mat-column-distances.ng-star-inserted > span").text.strip()
                        distance_str_list = distance_str.split(", ")
                        for distance_item in distance_str_list:
                            if "KM" in distance_item or "km" in distance_item or "k" in distance_item or "K" in distance_item:
                                if "," in distance_item:
                                    distance_item = distance_item.split(",")[0] #get first digit if fraction
                                    distances.append(int(distance_item)*1000)
                                else:
                                    try:
                                        distances.append(int(distance_item[:-2])*1000)
                                    except:
                                        pass
                            elif distance_item == "Halvmaraton":
                                distances.append(21097)
                            elif distance_item == "Maraton":
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
                        pass
                    #mappig out backyard ultras
                    if name.find("ackyard") != -1:
                        distances = "backyard"
                        race_type = "backyard"
                    else:
                        race_type = default_race_type

                    place = place.strip()
                    organizer = ""
                    website = ""
                    website_ai_fallback = name
                    # Extracting href from the anchor tag within the current row
                    race_href = row.select_one("td.mat-cell.cdk-cell.col-8.col-sm-6.col-md-4.col-lg-3.d-flex.align-items-center.cdk-column-name.mat-column-name.ng-star-inserted > a")['href']

                    #check if race exists in collection, otherwise continue
                    current_races = RaceCollection()
                    if current_races.exists_in_source(name, proper_date, url):
                        print(f'{name} already exists in source, continue')
                        continue

                    # Creating the complete URL
                    full_race_url = "https://terminlista.kondis.no/" + race_href

                    # Using Selenium to visit the race page
                    driver.get(full_race_url)
                    container_element = None
                    try:
                        # Find all container elements with the .container class
                        container_elements = wait.until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".container"))
                        )

                        # Select the second container element from the list
                        if len(container_elements) >= 2:
                            container_element = container_elements[1]
                            print("Second container element found")
                            # Now you can use container_element for further operations
                        else:
                            print("Second container element not found")
                    except TimeoutException:
                        print("Containers not found within 10 seconds")
                    # Find all anchor elements within the container
                    time.sleep(2)
                    print(f'container: {container_element}')
                    anchor_elements = wait.until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
                        )
                    # Iterate through anchor elements to find the one with text 'Hjemmeside'
                    hjemmeside_href = ""
                    print(anchor_elements)
                    for anchor_element in anchor_elements:
                        print(anchor_element.text)
                        if 'Hjemmeside' in anchor_element.text or 'Påmelding' in anchor_element.text or 'Facebook' in anchor_element.text:
                            # Extract the href attribute
                            hjemmeside_href = anchor_element.get_attribute("href")
                            print(hjemmeside_href)
                            break
                    website = hjemmeside_href
                    race = Race(date = proper_date, type =  race_type,  name = name, distance = distance_str, distance_m = distances, place = place, organizer = organizer, website = website, src_url = url, website_ai_fallback = website_ai_fallback)
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
        else:
            print("Error: Could not retrieve source URL:" + url )

        race_collection.append_or_create_source_json(subdomain)
        race_collection.append_or_create_source_json()
        print("Finished crawling " + url)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()


