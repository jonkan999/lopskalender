import requests
from bs4 import BeautifulSoup
import re
from scraper_package.race_classes import Race, RaceCollection


def main():

    subdomain = "trailrunningsweden"
    url = "https://www.trailrunningsweden.se/trailkalendern/"
    default_race_type = "trail"
    
    response = requests.get(url, 
                headers={'User-Agent': 'Mozilla/5.0'}
                )

    race_collection = RaceCollection()

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        events = soup.find_all("div", class_="event")
        for event in events:
            if "past_event" not in event["class"]:
                date_span = event.find("span", class_="evoet_dayblock evcal_cblock")
                month_name = date_span.get("data-smon")
                year_num = date_span.get("data-syr")
                months_dict = {
                    "januari": "01",
                    "februari": "02",
                    "mars": "03",
                    "april": "04",
                    "maj": "05",
                    "juni": "06",
                    "juli": "07",
                    "augusti": "08",
                    "september": "09",
                    "oktober": "10",
                    "november": "11",
                    "december": "12"
                }
                month_num = months_dict.get(month_name.lower(), "00")
                day = event.find("em", class_="date").text.strip().zfill(2)
                proper_date = f"{year_num}{month_num}{day}"
                name_span = event.find("span", class_="evoet_title evcal_desc2 evcal_event_title")
                name = name_span.text.strip()
                distance_str = ""
                distances = []
                try:
                    distance_span = event.find("span", class_="evcal_event_subtitle")
                    distance_str = distance_span.text.strip()
                    for distance_item in distance_str.split(", "):
                        if "KM" in distance_str or "km" in distance_str or "k" in distance_str or "K" in distance_str:
                            if "," in distance_item:
                                distance_item = distance_item.split(",")[0] #get first digit if fraction
                                distances.append(int(distance_item)*1000)
                            else:
                                try:
                                    distances.append(int(distance_item[:-2])*1000)
                                except:
                                    pass
                        elif "MILES" in distance_str:
                            try:
                                for match in re.findall(r"(\d+)\s*KM", distance_str):
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
                    distances = ["backyard"]
                    race_type = "backyard"
                else:
                    race_type = default_race_type
                
                distances.sort()
                place=name
                organizer = ""


                website_a = event.find("a", class_="evcal_evdata_row evo_clik_row")
                website = website_a.get("href") if website_a else ""
                website_ai_fallback = name + " " + distance_str
                
                race = Race(date = proper_date, type =  race_type,  name = name, distance = distance_str, distance_m = distances, place = place, organizer = organizer, website = website, src_url = url, website_ai_fallback = website_ai_fallback)
                
                ### STANDARD ENDING ###
                race.add_id('extract')
                race_collection.add_race_if_doesnt_exist('extraction/sourced_races.json', race)
    else:
        print("Error: Could not retrieve source URL:" + url )

    race_collection.append_or_create_source_json(subdomain)
    race_collection.append_or_create_source_json()
    print("Finished crawling " + url)

if __name__ == "__main__":
    main()
