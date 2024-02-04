import json
from scraper_package.race_classes import Race, RaceCollection  # Replace 'your_module' with the actual module name containing RaceCollection

def process_transformed_races(transformed_races_file, images_file, approved_races_raw_file):
    # Load transformed races from JSON file
    with open(transformed_races_file, 'r', encoding='utf-8') as file:
        transformed_races = json.load(file)

    # Create two dictionaries to store the processed data
    images_dict = {'images': []}
    approved_races_raw = []


    # Create a RaceCollection instance
    source_race_collection = RaceCollection()

    # Iterate through transformed races
    for race_info in transformed_races:
        # Extract the required fields for the race collection
        source_race_data = {
            'date': race_info.get('date'),
            'type': race_info.get('type'),
            'name': race_info.get('name'),
            'distance': race_info.get('distance'),
            'distance_m': race_info.get('distance_m'),
            'place': race_info.get('place'),
            'organizer': race_info.get('organizer'),
            'website': race_info.get('website'),
            'website_ai_fallback': race_info.get('website_ai_fallback'),
            'src_url': race_info.get('src_url'),
            'new_version': True,
            'id': race_info.get('id'),
            'is_transformed': True,
            'is_approved': True,
        }

        # Add the race to the RaceCollection
        source_race_collection.add_race_if_doesnt_exist('extraction/sourced_races.json',Race(**source_race_data))

        # Extract the required fields for the images dictionary
        image_data = {
            'name': race_info.get('name'),
            'id': race_info.get('id'),
            'images': race_info.get('images', []),
        }

        # Append image_data to the images dictionary
        images_dict['images'].append(image_data)

                # Extract specific keys for approved races raw data
        approved_race_raw_data = {
            'date': race_info.get('date'),
            'type': race_info.get('type'),
            'name': race_info.get('name'),
            'distance': race_info.get('distance'),
            'distance_m': race_info.get('distance_m'),
            'place': race_info.get('place'),
            'organizer': race_info.get('organizer'),
            'website': race_info.get('website'),
            'website_ai_fallback': race_info.get('website_ai_fallback'),
            'src_url': race_info.get('src_url'),
            'created_date': race_info.get('created_date'),
            'updated_date': race_info.get('updated_date'),
            'id': race_info.get('id'),
            'extract_id': race_info.get('extract_id'),
            'contents': race_info.get('contents'),
            'race_categories': race_info.get('race_categories'),
            'long_summary': race_info.get('summary'),
            'summary': race_info.get('short_summary'),
            'ai_name_guess': race_info.get('ai_name_guess'),
            'latitude': race_info.get('latitude'),
            'longitude': race_info.get('longitude'),
            'county': race_info.get('county'),
            'is_approved': True,
        }

        # Append the approved race raw data to the list
        approved_races_raw.append(approved_race_raw_data)

    # Append the processed data to the source files
    source_race_collection.append_or_create_source_json()
    append_or_create_json(images_file, images_dict)
    
    # Append the approved races raw data to approved_races_raw.json
    append_or_create_json(approved_races_raw_file, approved_races_raw)

def append_or_create_json(file_path, data):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        existing_data.extend(data)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False)
    except:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)

# Example usage
process_transformed_races('transformed_races.json', 'images.json', 'approved_races_raw.json')
