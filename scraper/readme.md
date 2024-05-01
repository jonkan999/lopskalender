-- Activate venv and move to scraper folder:

scraper\venv\Scripts\Activate.ps1
cd scraper

or:
scraper\venv\Scripts\Activate.ps1
cd scraper
python main_scraper.py

These files are meant to run in the order:

-- Main scraper script that scrapes content from source pages, compares to previous loads, stores new races, transforms new races and puts them up for staging.

python main_scraper.py

-- Gui that looks att all staged races and compares them to races already in production on the same day. Meant to be a checking tool so we dont load duplicate races.

python approvalGUI.py

-- Generates individual race pages per race based on a jinja template
--if you want to run only races that is not already in main all_races json, i.e newly collected run this and thats also by default
python generate_pages.py

--if you want to load all current races with images:
python generate_pages.py 0

-- Update main list html
python update_current_races.py
python update_main_list.py

--- Update seo folders
python update_seo_folders.py

-- git ocmmand
git add --all :!images.json
git commit -m "adding new races"
git push

python generate_pages.py
python update_current_races.py
python update_main_list.py
python update_seo_folders.py
git add --all :!images.json
git commit -m "adding new races"
git push
