import json
from datetime import datetime
from scraper_package.race_classes import Race, RaceCollection
import os



def add_transformed_and_approved(races):
    for race in races:
        race['is_transformed'] = True
        race['is_approved'] = True
    return races

def main():
    # Read all_races_w_formatted_summary.json
    with open('all_races_w_formatted_summary.json', 'r', encoding='utf-8') as file:
        all_races_data = json.load(file)

    # Create Race objects from the data
    all_races = [Race(**race_info, website_ai_fallback = None) for race_info in all_races_data]

    # Add is_transformed and is_approved to all_races
    all_races_data = add_transformed_and_approved(all_races_data)

    # Read sourced_races.json
    sourced_races_file_path = 'sourced_races.json'
    sourced_races_data = []

    if os.path.exists(sourced_races_file_path):
        with open(sourced_races_file_path, 'r', encoding='utf-8') as file:
            sourced_races_data = json.load(file)

        # Add is_transformed and is_approved to sourced_races
        sourced_races_data = add_transformed_and_approved(sourced_races_data)

    # Concatenate sourced_races below all_races
    all_races_data.extend(sourced_races_data)

    # Write the combined data to sourced_races.json
    with open(sourced_races_file_path, 'w', encoding='utf-8') as file:
        json.dump(all_races_data, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
