import os
import json
from datetime import datetime

def load_json_with_keys(file_path, selected_keys):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    filtered_data = [{key: race[key] for key in selected_keys} for race in data if all(key in race for key in selected_keys)]
    return filtered_data

def load_json(file_path, selected_keys=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if selected_keys:
        return [{key: race[key] for key in selected_keys} for race in data]
    else:
        return data

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def append_approved_races(current_races, approved_races_raw):
    for race in approved_races_raw:
        race_id = race.get('id')
        if race_id is not None and race_id not in {r.get('id') for r in current_races}:
            current_races.append(race)

def sort_and_save_all_races(all_races_file_path, current_races):
    # Sort the races by date, lat, and log
    current_races.sort(key=lambda x: (x.get('date'), x.get('latitude'), x.get('longitute')))
    
    # Save the sorted races back to the file
    save_json(all_races_file_path, current_races)

def main():
    # File paths
    all_races_file_path = "../all_races_w_formatted_summary.json"
    approved_races_raw_file_path = "approved_races_raw.json"

    # Rename a copy of the file with a timestamp
    timestamp = datetime.now().strftime("%y%m%d")
    copy_file_path = f"../all_races_w_formatted_summary_{timestamp}.json"
    os.rename(all_races_file_path, copy_file_path)

    # Read the complete json as a dictionary
    current_races = load_json(copy_file_path)

    # Specify the keys you want to keep
    selected_keys = [
        'date', 'type', 'name', 'distance',
        'distance_m', 'place', 'latitude', 'longitude', 
        'organizer', 'website', 'src_url', 'id', 'summary', 'county'
    ]

    # Check if 'summary' is present in all races in approved_races_raw.json
    if all(key in load_json(approved_races_raw_file_path)[0] for key in selected_keys):
        # Read in approved_races_raw.json and append races with unique IDs
        approved_races_raw = load_json_with_keys(approved_races_raw_file_path, selected_keys)
        append_approved_races(current_races, approved_races_raw)
    
    # Sort and save the updated races
    sort_and_save_all_races(all_races_file_path, current_races)

if __name__ == "__main__":
    main()
