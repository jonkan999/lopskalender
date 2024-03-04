import json
from scraper_package import transform_module
from configuration.keys import GOOGLE_GEOCODING_API_KEY as goog_access_token
from configuration.keys import OPENAI_KEY as openai_access_token
from scraper_package.race_classes import Race, RaceCollection
from configuration.vars import lang_val, lang_code, custom_search_cx, lr

def transform_and_store_race(race, costometer, openai=True):
    try:
        print(f"""
              TRANSFORMING----------------------
              ----------------------------------
              {race["name"]}
              ----------------------------------
                """)
        # Check if "park run" or "parkrun" is in the race name, and skip transformation if true
        if "park run" in race["name"].lower() or "parkrun" in race["name"].lower():
            print(f"Skipping transformation for race with name: {race['name']} because it contains 'park run' or 'parkrun'")
            in_race = Race(**race)
            in_race.set_is_transformed(in_bool=True, update_source_json=True)
            return race
        # Get website if not allowed or missing
        print("getting website")
        race["website"] = transform_module.check_allowed_url(race["website"], race["website_ai_fallback"], goog_access_token, custom_search_cx, lr)
        #race["website"] = transform_module.check_allowed_url_get_goog(race["website"], race["website_ai_fallback"])
        #race["website"] = transform_module.check_allowed_url_get_bing(race["website"], race["website_ai_fallback"])
        print("done getting website")

        # Get website contents
        print("getting website content")
        contents = transform_module.get_website_contents(race["website"])
        race["contents"] = contents
        print("done getting website content")

        # Getting images
        image_search_query = f'"{race["name"]} {transform_module.process_url(race["website"])}"'
        image_url_list = transform_module.get_images_selenium(image_search_query)
        print("got images:")
        print(image_url_list)
        images = [transform_module.convert_and_compress_image(img, max_size_kb=200) for img in image_url_list]
        selected_images = [img for img in images if img is not None][:6]
        transform_module.add_or_update_object(race["name"], race["id"], selected_images, "images.json")
        print("done with images")

        # Extract specific fields
        title = race['contents']['title']
        description = race['contents']['description']
        h1 = race['contents']['h1']
        paragraphs = race['contents']['p'][0] if race['contents']['p'] else ""
        h2 = race['contents']['h2'][0] if race['contents']['h2'] else ""

        # Map distances
        race["race_categories"] = transform_module.race_category_mapping(race["distance_m"], race["type"])
        print(race["race_categories"])

        if openai:
          # Generate summary prompt
          summary_prompt = f"Given this:\n\nTitle: {title}\nDescription: {description}\nH1: {h1}\nH2: {h2}\np-element: {paragraphs}\n\n Make a summary of the race in {lang_val}. Pretend that you are a running race director. Write a description in a couple of paragraphs that describes a race like that, you are allowed to freestyle a bit. Don't use HTML elements like Title:, H1:, or H2: in the text. Also emphasize that the race includes the following race categories/distances: {race['race_categories']} . And of this type: {race['type']}"
          race["long_summary"], costometer = transform_module.get_completion(prompt=summary_prompt, costometer=costometer, openai_key=openai_access_token)

          if race['long_summary']:
              short_summary_prompt = f"Given this:{race['long_summary']} Pretend that you are a running race director and write a shorter summary in {lang_val} of no more than 500 characters. Also emphasize that the race includes the following race categories/distances: {race['race_categories']} . And of this type: {race['type']}"
              race["summary"], costometer = transform_module.get_completion(prompt=short_summary_prompt, costometer=costometer, openai_key=openai_access_token)
          else:
              race["summary"] = None

          name_prompt = f"Given this:\n\nTitle: {title}\nDescription: {description}\nH1: {h1}\nH2: {h2}\n\n Pretend that you are the race director for this running race and give it a name in {lang_val} and using no more than 3 words"
          race["ai_name_guess"], costometer = transform_module.get_completion(prompt=name_prompt, costometer=costometer, openai_key=openai_access_token)
        else:
            race["ai_name_guess"] = None
        # Get lat and long from google geocoding API using search strings in order of preference
        search_strings = [
            race["place"],
            race["name"],
            race["website"],
            race["website_ai_fallback"],
            race["contents"]["title"],
            race["contents"]["h1"],
            race["ai_name_guess"]
        ]

        # Get coordinates for the first successful search string
        latitude, longitude = transform_module.get_lat_long_goog(goog_access_token, *search_strings)
        print("done geocoding")
        race["latitude"] = latitude
        race["longitude"] = longitude

        #if lang_val == "Swedish":
        # Get swedish counties for found coordinates
        if latitude != 0:
            race["county"] = transform_module.find_county(latitude, longitude)
        else:
            race["county"] = None

        #get id from races in staged_for_aproval
        staging_path="staged_for_approval.json"
        print("getting id from staged_for_approval")
        if race["id"] not in transform_module.get_all_ids_from_json(staging_path):
            print("appending to staged_for_approval")
            in_race = Race(**race)
            race_collection = RaceCollection()
            race_collection.races.append(in_race)
            print("appending to staged_for_approval")
            race_collection.append_or_create_json(staging_path)
            #updating race id in source json
            in_race.set_is_transformed(in_bool = True, update_source_json = True)

        return race

    except Exception as e:
        print(f"Error transforming race: {e}")
        return None
    
if __name__ == "__main__":
    # Hardcoded test race
    test_race = {
        "date": "20240525",
        "type": "road",
        "name": "Halvtovlan",
        "distance": "Halvtovlan",
        "distance_m": [6000],
        "place": "Bromma",
        "organizer": "",
        "website": "https://www.jogg.se//Tavling/Tavling.aspx?id=657417",
        "website_ai_fallback": "Halvtovlan Bromma 6,00 km",
        "src_url": "https://www.jogg.se/Kalender/Tavlingar.aspx?aar=2024&mon=13&fdist=0&tdist=1000&type=0&country=1&region=0&tlopp=False&relay=False&surface=asf&tridist=0&title=1",
        "created_date": "2023-12-07 18:17:00",
        "updated_date": "2023-12-07 18:17:00",
        "id": "halvtovlan_20240525_httpswwwjoggsekalendertavlingaraspxaar2024mon13fdist0tdist1000type0country1region0tloppfalserelayfalsesurfaceasftridist0title1",
        "extract_id": "afa805ac-583d-4e14-b2d9-b4ba7e39e406"
    }

    # Run transformation on the test race
    transformed_test_race = transform_and_store_race(test_race,costometer=0, openai=False)

    if transformed_test_race:
        print("Transformed Test Race:")
        print(transformed_test_race)
    else:
        print("Error transforming test race.")