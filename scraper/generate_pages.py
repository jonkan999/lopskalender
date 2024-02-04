
import json
from datetime import datetime
from page_generator_package.page_generator import PageGenerator
from page_generator_package.functions import map_distance
import sys
import yaml

current_date = datetime.now().strftime("%Y%m%d")
print(current_date)

def read_all_events(event_path, only_current):
    try:
        with open(event_path, 'r', encoding='utf-8') as all_races_file:
            unfiltered_races = json.load(all_races_file)
            if only_current:
                filtered_races = [race for race in unfiltered_races if race.get("date", "") >= current_date]
                return filtered_races
            else:
                return unfiltered_races
    except FileNotFoundError:
        print(f"File {event_path} not found.")
        return []

def read_all_generateable_events(generateable_event_path, only_current):
    try:
        with open(generateable_event_path, 'r', encoding='utf-8') as races_file:
            races_data = json.load(races_file)
            # Filter races with 'long_summary' key
            if only_current:
                races_data = [race for race in races_data if race.get("date", "") >= current_date]
            races_with_long_summary = [race for race in races_data if 'long_summary' in race]
            return races_with_long_summary
    except FileNotFoundError:
        print(f"File {generateable_event_path} not found.")
        return []

def read_all_images(image_path):
    try:
        with open('images.json', 'r', encoding='utf-8') as images_file:
            images_data = json.load(images_file)
            return images_data
    except FileNotFoundError:
        print(f"File {image_path} not found.")
        return []

def join_images_and_events(events, images, consider_only_new, current_events):
    if consider_only_new:
        current_events_ids = [event["id"] for event in current_events]
        porposed_events_ids = [event["id"] for event in events]
        events = [event for event in events if event["id"] not in current_events_ids]
    print(f"Number of events to generate: {len(events)}")
    joined_data = []

    for race in events:
        race_id = race["id"]

        for image in images:
            if type(image) == str:
                continue
            image_id = image["id"]
            
            # Check if race_id is equal to image_id
            if race_id == image_id:
                joined_data.append({**race, 'images': image['images']})
                print("match")
                break  # No need to continue checking once a match is found
    print(f"Number of events with images: {len(joined_data)}")
    return joined_data

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        is_consider_only_new = bool(int(sys.argv[1]))
    else:
        is_consider_only_new = True
    print(f"Consider only new: {is_consider_only_new}")
    # Rest of the code...
    #configuration
    config_file = "../collection_configuration/page_config.yaml"
    sitemap_path = "../sitemap.xml"
    event_path = '../all_races_w_formatted_summary.json'
    generateable_event_path = "approved_races_raw.json"
    image_path = "images.json"
    with open("../collection_configuration/general_config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) 

    

    #read data
    all_events = read_all_events(event_path, only_current = True) #only_current, I.e only events that has not already been
    events = read_all_generateable_events(generateable_event_path = generateable_event_path, only_current = True)
    images = read_all_images(image_path)
    events_w_images = join_images_and_events(events, images, consider_only_new = is_consider_only_new, current_events = all_events) #if consider_only_new, only events that has not already been generated
    print(f"Number of events to generate: {len(events_w_images)}")
    #generate individual event pages
    for event in events_w_images:
        print(f"Generating page for {event['name']}")
        event['display_distances'] = map_distance(sorted(event['distance_m']),event['type'],config['distance_mapping'],config['distance_units'])
        event['display_distances'] = ', '.join(map(str, event['display_distances']))
        #generate page
        page_generator = PageGenerator(config_file, event, sitemap_path, event["images"])
        page_generator.generate_page()
        page_generator.update_sitemap()
        page_generator.update_current_event(all_events)
    
    # Save the modified all_races_data
    try:
        all_events = sorted(all_events, key=lambda x: (x["date"], x["longitude"], x["latitude"]))
        with open('../all_races_w_formatted_summary.json', 'w', encoding='utf-8') as all_races_file:
            json.dump(all_events, all_races_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("File '../all_races_w_formatted_summary.json' not found.")

    print("HTML files generated successfully.")