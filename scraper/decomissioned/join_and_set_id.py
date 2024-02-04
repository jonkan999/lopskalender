import json

# Read the lists from the files
with open('approved_races_raw.json', 'r', encoding='utf-8') as file:
    approved_races_raw = json.load(file)

with open('current_active_races.json', 'r', encoding='utf-8') as file:
    current_active_races = json.load(file)

for a_race in approved_races_raw:
    for c_race in current_active_races:
            if a_race['name'] == c_race['name'] \
            and a_race['date'] == c_race['date'] \
            and a_race['distance'] == c_race['distance'] \
            and a_race['src_url'] == c_race['src_url']:
                a_race['id'] = c_race['id']


# Save the updated approved_races_raw list to a new file or overwrite the existing one
with open('updated_approved_races_raw.json', 'w', encoding='utf-8') as file:
    json.dump(approved_races_raw, file, ensure_ascii=False, indent=2)
