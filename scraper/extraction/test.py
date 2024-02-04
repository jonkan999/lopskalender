
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

# Set up the Selenium webdriver (make sure you have the appropriate webdriver installed)
options = Options()
options.add_argument("--headless=new")
options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'")
driver=webdriver.Chrome(options=options)
# Open the URL in the browser
url = "https://terminlista.kondis.no/l%C3%B8ping?underlag=asfalt&pagesize=200&page=1"
driver.get(url)

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

# Close the browser
driver.quit()

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

            print(proper_date)
            name = row.select_one("td.mat-cell.cdk-cell.col-8.col-sm-6.col-md-4.col-lg-3.d-flex.align-items-center.cdk-column-name.mat-column-name.ng-star-inserted > a").text.strip()
            place = row.select_one("td.mat-cell.cdk-cell.col-3.col-md-2.d-none.d-sm-flex.align-items-center.cdk-column-location.mat-column-location.ng-star-inserted > span").text.strip()
            distance_str = row.select_one("td.mat-cell.cdk-cell.col-md-2.col-lg-3.d-none.d-md-flex.align-items-center.cdk-column-distances.mat-column-distances.ng-star-inserted > span").text.strip()
            # Print or store the extracted information
            print(f"Date: {date_text}")
            print(f"Name: {name}")
            print(f"Place: {place}")
            print(f"Distance: {distance_str}")
            print("-" * 30)
    else:
        print("Tbody not found within the main table.")
else:
    print("Main table not found on the page.")
