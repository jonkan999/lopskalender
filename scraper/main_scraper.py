# File: C:\Users\Joel\loppkartan.se\scraper\run_all_scripts.py
import sys
from configuration.scraper_scripts import run_all_scraper_scripts
from scraper_package.race_classes import Race, RaceCollection
from transform_race import transform_and_store_race

if __name__ == "__main__":
    try:
        run_all_scraper_scripts()
    except Exception as e:
        print(e)
        sys.exit()

    # Load all not transformed from source
    untransformed_races = RaceCollection()
    untransformed_races.load_not_transformed_from_source_json()
    
    # Set a limit on the number of races to process at a time
    max_races_to_process = 50
    races_to_process = untransformed_races.races[:max_races_to_process]
    
    costometer = 0
    
    # Transform the selected races
    print(races_to_process)
    try:
        for i, race in enumerate(races_to_process):
            print(f"""
            TRANSFORMING----------------------
            ----------------------------------
            {race["name"]}
            RACES TRANSFORMED: {i + 1} / {max_races_to_process}
            ----------------------------------
            """)
            transform_and_store_race(race.data, costometer, openai=True)
        
        print(f"""
        DONE TRANSFORMING----------------------
        ----------------------------------
        RACES TRANSFORMED: {i + 1} / {max_races_to_process}
        ----------------------------------
        """)
    except NameError:
        print("No new races to process. Exiting...")
        sys.exit()
