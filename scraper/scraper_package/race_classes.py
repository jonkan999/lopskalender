import os
import json
import re
from datetime import datetime
import uuid
from difflib import SequenceMatcher  # Import SequenceMatcher for string similarity

source_file_path = 'extraction/sourced_races.json'

class Race:
    def __init__(self, date, type,  name, distance, distance_m, place, organizer, website, src_url, website_ai_fallback = None, created_date=None, updated_date=None, **kwargs):
        self.data = {
            "date": date,
            "type": type,
            "name": name,
            "distance": distance,
            "distance_m": distance_m,
            "place": place,
            "organizer": organizer,
            "website": website,
            "website_ai_fallback": website_ai_fallback,
            "src_url": src_url,
            ## Add the created and updated dates if not provided defaults to current date
            "created_date": created_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_date": updated_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": self.generate_id(name, date, src_url),
            **kwargs
        }

    def similar_race_ratio(self, in_name):
        return SequenceMatcher(None, self.data["name"], in_name).ratio()

    def generate_id(self, name, proper_date, src_url):
        # Use regex to replace dashes and special characters with "-"
        id_string = f"{name}_{proper_date}_{src_url}"
        id_string = re.sub(r'[^\w\s-]', '', id_string)
        id_string = re.sub(r'[-\s]+', '-', id_string)
        return id_string.lower()

    def update_updated_date(self):
        self.data["updated_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_id(self, id_prefix):
        self.data[f'{id_prefix}_id'] = str(uuid.uuid4())

    def update_source_json(self, key, value):
        """
        Update the source JSON file with the modified data.

        Parameters:
            - key: The key to update in the JSON file.
            - value: The new value to set for the specified key.
        """
        

        # Load the source JSON data
        with open(source_file_path, encoding='utf-8') as f:
            source = json.load(f)

        # Update the corresponding item in the source JSON data
        for obj in source:
            if 'id' in self.data and self.data['id'] == obj.get('id'):
                obj[key] = value

        # Save the updated source JSON data
        with open(source_file_path, 'w', encoding='utf-8') as f:
            json.dump(source, f, ensure_ascii=False)

    def set_is_transformed(self, in_bool: bool = True, update_source_json: bool = False):
        # Set the "is_transformed" key in the data attribute to the specified boolean value.
        self.data["is_transformed"] = in_bool

        if update_source_json:
            # Update the source JSON file with the modified data
            self.update_source_json('is_transformed', in_bool)

    def set_is_approved(self, in_bool: bool = True, update_source_json: bool = False):
        self.data["is_approved"] = in_bool

        if update_source_json:
            # Update the source JSON file with the modified data
            self.update_source_json('is_approved', in_bool) 

    def set_is_discarded(self, in_bool: bool = True, update_source_json: bool = False):
        self.data["is_discarded"] = in_bool

        if update_source_json:
            # Update the source JSON file with the modified data
            self.update_source_json('is_discarded', in_bool) 
    
    def remove_from_file(self, file_path):
        """
        Remove the race from the specified JSON file.

        Parameters:
            - file_path: The path to the JSON file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                race_data = json.load(file)

            # Remove the race from the data list
            race_data = [race for race in race_data if race.get('id') != self.data.get('id')]

            # Save the updated data back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(race_data, file, ensure_ascii=False)

            print(f"Race '{self.data['name']}' removed from {file_path}")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")

    ## Override the default __getitem__ method so that we can access the data dictionary directly
    def __getitem__(self, key):
        return self.data.get(key, None)

class RaceCollection:
    def __init__(self):
        self.races = []

    def load_from_json(self, file_path, filter_transformed=None, filter_approved=None):
        with open(file_path, 'r', encoding="utf-8") as file:
            race_data = json.load(file)
            for race_info in race_data:
                is_transformed = race_info.get("is_transformed", False)
                is_approved = race_info.get("is_approved", False)

                # Check if the race meets the specified filtering conditions
                # If filter_transformed is None, include all races, otherwise check is_transformed
                # If filter_approved is None, include all races, otherwise check is_approved
                if (filter_transformed is None or is_transformed == filter_transformed) \
                        and (filter_approved is None or is_approved == filter_approved):
                    # Add the race to the collection if it passes the filters
                    race = Race(**race_info)
                    self.races.append(race)

    def save_to_json(self, file_path):
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump([race.data for race in self.races], file, ensure_ascii=False)

    def pop_race(self):
        return self.races.pop()
    
    def load_not_transformed_from_source_json(self):
        # Call the load_from_json method with the specified file path and filter_transformed set to True
        self.load_from_json(source_file_path, filter_transformed=False, filter_approved=None)
    
    def load_from_source_json(self):
        self.load_from_json(source_file_path)



    def set_is_transformed(self):
        for race in self.races:
            race.set_is_transformed()

    def set_is_approved(self):
        for race in self.races:
            race.set_is_approved()

    def filter_races(self, filter_col, filter_value):
        filtered_races = [race.data for race in self.races if race.data.get(filter_col) == filter_value]
        return filtered_races
    
    def append_or_create_json(self, filename):
        # Check if the file exists
        try:
            # If the file exists, load the existing data and append to it
            with open(filename, "r", encoding='utf-8') as file:
                existing_data = json.load(file)

            existing_data.extend([race.data for race in self.races])

            # Write the combined data back to the file
            with open(filename, "w", encoding='utf-8') as file:
                json.dump(existing_data, file, ensure_ascii=False)
        except FileNotFoundError:
            # If the file doesn't exist, create a new file with the provided data
            with open(filename, "w", encoding='utf-8') as file:
                json.dump([race.data for race in self.races], file, ensure_ascii=False)
    
    def append_or_create_source_json(self, subdomain=None):
        if subdomain:
            self.append_or_create_json(f"extraction/sourced_races_{subdomain}.json")
        else:
            self.append_or_create_json(f"extraction/sourced_races.json")

    def exists_in_source(self, name, date, src_url):
        # Load the source JSON data
        self.load_from_source_json()
        for race in self.races:
            if (
                race.data.get('date') == date
                and race.data.get('name') == name
                and race.data.get('src_url')[:-3] == src_url[:-3]
            ):
                print(race.data.get('name') + " already exists.")
                return True
            elif race.data.get('date') == date and (
                SequenceMatcher(None, race.data.get('name'), name).ratio() > 0.5
            ):
                print(race.data.get('name') + " and " + name + " too similar.")
                return True
            
    def clean_races(self):
        self.races = []

    def add_race_if_doesnt_exist(self, races_json_path, new_race):
        # Load existing races from the collection
        existing_races = [race.data for race in self.races]

        # Load races from the specified JSON path
        if os.path.exists(races_json_path):
            with open(races_json_path, 'r', encoding="utf-8") as file:
                existing_races.extend(json.load(file))

        # Check if the new race already exists
        if self.check_existing_race(new_race.data, existing_races):
            print(f"Race '{new_race.data['name']}' already exists.")
            return False

        # If the race doesn't exist, add it to the collection
        self.races.append(new_race)
        print(f"Race '{new_race.data['name']}' added to the collection.")
        return True

    def clean_races(self):
        self.races = []

        # Check if
    def check_existing_race(self, event_data, existing_races):
        date, name, distance, src_url = (
            event_data['date'],
            event_data['name'],
            event_data['distance'],
            event_data['src_url'],
        )

        for race in existing_races:
            if (
                race.get('date') == date
                and race.get('name') == name
                and race.get('distance') == distance
                and race.get('src_url')[:-3] == src_url[:-3]
            ):
                print(race.get('name') + " already exists.")
                return True
            elif race.get('date') == date and (
                SequenceMatcher(None, race.get('name'), name).ratio() > 0.5
            ):
                print(race.get('name') + " and " + name + " too similar.")
                return True

        return False
