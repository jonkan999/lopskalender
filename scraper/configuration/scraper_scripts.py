### INPUT SCRIPTS ###

# program_configuration.py
import sys

from extraction import (
    extract_data_fri_Indoor_2024,
    extract_data_jogg_trail,
    extract_data_jogg_road,
    extract_data_trailkalendern,
)
from scraper_package.race_classes import Race, RaceCollection
from transform_race import transform_and_store_race

def run_all_scraper_scripts():
    extract_data_fri_Indoor_2024.main()
    extract_data_jogg_road.main()
    extract_data_jogg_trail.main()
    extract_data_trailkalendern.main()

if __name__ == "__main__":
    try:
        run_all_scraper_scripts()
    except Exception as e:
        print(e)
        sys.exit()
