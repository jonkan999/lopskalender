import json
from scraper_package import scraper_module
from scraper_package import transform_module

def transform_records(json_file):
    # Read the JSON file as a dictionary
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Set is_transformed to True for all records
    for entry in data:
        entry['is_approved'] = True

    return data

# Replace 'sourced_races.json' with the actual path to your JSON file
json_file_path = 'transformed_races.json'
data = transform_records(json_file_path)
scraper_module.create_json(json_file_path, data)
