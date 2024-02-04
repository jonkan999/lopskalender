from scraper_package import scraper_module
from scraper_package import transform_module
import uuid
from datetime import datetime

def generate_unique_id():
    # Generate a unique hash here (replace this with your hash generation logic)
    unique_id = str(uuid.uuid4())
    return unique_id

def filter_dict(original_dict, keys_to_extract):
    filtered_dict = {key: original_dict[key] for key in keys_to_extract if key in original_dict}
    return filtered_dict

keys_to_extract = ['date', 'month', 'day', 'type', 'name', 'distance', 'distance_m',
                   'place', 'latitude', 'longitude', 'organizer', 'website', 'src_url',
                   'short_summary', 'county']

# Filter the dictionary

races = transform_module.import_not_approved("transformed_races.json")
filtered_races = []
for i in range(len(races)):
    filtered_race_dict = filter_dict(races[i], keys_to_extract)
    print(filtered_race_dict)
    filter_dict(filtered_race_dict, keys_to_extract)
    filtered_race_dict["new_version"] = True
    filtered_race_dict["id"] = generate_unique_id()
    filtered_race_dict["summary"] = filtered_race_dict["short_summary"]
    filtered_races.append(filtered_race_dict)

#sort
filtered_races = sorted(filtered_races, key=lambda r: (r["date"], r["longitude"], r["latitude"]))

# Assuming filtered_races is your data
current_date = datetime.today().strftime("%Y-%m-%d")
filename = f"old_format_races_{current_date}.json"

scraper_module.create_json(filename, filtered_races)