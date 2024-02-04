import json
from scraper_package import scraper_module
from scraper_package import transform_module

races = transform_module.import_json('transformed_races.json')

print(races[0])
print(races[0]['extract_id'])
scraper_module.update_source(races,'sourced_races.json','extract_id','is_transformed', True)

