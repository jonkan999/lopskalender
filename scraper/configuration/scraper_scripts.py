### INPUT SCRIPTS ###

# program_configuration.py
import sys

from extraction import (
    extract_data_kondis_road,
    extract_data_friidrett_road,
    extract_data_friidrett_trail,
    extract_data_friidrett_terrain,
    extract_data_friidrett_relay
)
from scraper_package.race_classes import Race, RaceCollection
from transform_race import transform_and_store_race

def run_all_scraper_scripts():
    extract_data_friidrett_terrain.main()
    extract_data_friidrett_trail.main()
    extract_data_kondis_road.main()
    extract_data_friidrett_road.main()
    #extract_data_friidrett_relay.main()

if __name__ == "__main__":
    try:
        run_all_scraper_scripts()
    except Exception as e:
        print(e)
        sys.exit()
