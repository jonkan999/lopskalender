import os
import shutil
import yaml
from datetime import datetime

def clean_filename(name):
    name = name.replace('-', ' ').replace('/', '').replace('å', 'a').replace('ä', 'a').replace('ö', 'o').replace('Å', 'A').replace('Ä', 'A').replace('Ø', 'O').lower().replace('ø', 'o').replace('ö', 'o')
    return '-'.join(name.split()).lower()

# Read the general configuration file
with open("../collection_configuration/general_config.yaml", 'r', encoding='utf-8') as f:
  config = yaml.safe_load(f)

# Define the parent folder
parent_folder = "../"

# Create a folder called "lan"
lan_folder = os.path.join(parent_folder, "lan")
os.makedirs(lan_folder, exist_ok=True)

# Create a folder called "category"
category_folder = os.path.join(parent_folder, "category")
os.makedirs(category_folder, exist_ok=True)

# Create a folder called "type"
type_folder = os.path.join(parent_folder, "type")
os.makedirs(type_folder, exist_ok=True)

# Iterate over the county mapping
sitemap_string = ""

for county, county_value in config["county_mapping"].items():
  print(f"Creating folder for {county}")
  # Create a folder with the same name as the county within the "lan" folder
  folder_name = clean_filename(county)
  folder_path = os.path.join(lan_folder, folder_name)
  os.makedirs(folder_path, exist_ok=True)

  # Copy lopsliste.html to index.html in the folder
  shutil.copy2("../lopsliste.html", os.path.join(folder_path, "index.html"))

  # Replace the field containing the county selector and add "selected"
  with open(os.path.join(folder_path, "index.html"), 'r+', encoding='utf-8') as file:
    string_to_replace = f"""<option value="{county}">{county}</option>"""
    string_to_replace_with = f"""<option value="{county}" selected>{county}</option>"""
    content = file.read()
    content = content.replace(string_to_replace, string_to_replace_with)
    content = content.replace(config["title_find"], config["seo_county_title"] % county_value)
    content = content.replace(config["description"], config["seo_county_description"] % county_value)
    file.seek(0)
    file.write(content)
    file.truncate()


  # Generate sitemap string
  sitemap_string += f"<url>\n"
  sitemap_string += f"  <loc>https://lopskalender.com/lan/{folder_name}/index.html</loc>\n"
  # Get the current date
  current_date = datetime.now().date()

  # Format the date as "YYYY-MM-DD"
  formatted_date = current_date.strftime("%Y-%m-%d")

  sitemap_string += f"  <lastmod>{formatted_date}T14:19:49+00:00</lastmod>\n"
  sitemap_string += f"  <priority>0.75</priority>\n"
  sitemap_string += f"</url>\n"

for category, category_data in config["category_mapping"].items():
    print(f"Creating folder for {category}")
    
    # Create a folder with the same name as the category within the "category" folder
    folder_name = clean_filename(category)
    folder_path = os.path.join(category_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Copy lopsliste.html to index.html in the folder
    shutil.copy2("../lopsliste.html", os.path.join(folder_path, "index.html"))

    # Replace the field containing the category selector and add "selected"
    with open(os.path.join(folder_path, "index.html"), 'r+', encoding='utf-8') as file:
        string_to_replace = f"""<option value="{category}">{category}</option>"""
        string_to_replace_with = f"""<option value="{category}" selected>{category}</option>"""
        content = file.read()
        content = content.replace(string_to_replace, string_to_replace_with)
        content = content.replace(config["title_find"], config["seo_category_title"] % category_data)
        content = content.replace(config["description"], config["seo_category_description"] % category_data)
        file.seek(0)
        file.write(content)
        file.truncate()

    # Generate sitemap string
    sitemap_string += f"<url>\n"
    sitemap_string += f"  <loc>https://lopskalender.com/category/{folder_name}/index.html</loc>\n"

    # Get the current date
    current_date = datetime.now().date()

    # Format the date as "YYYY-MM-DD"
    formatted_date = current_date.strftime("%Y-%m-%d")

    sitemap_string += f"  <lastmod>{formatted_date}T14:19:49+00:00</lastmod>\n"
    sitemap_string += f"  <priority>0.75</priority>\n"
    sitemap_string += f"</url>\n"

for checkbox_config in config["checkbox_mapping"]:
    container_id = checkbox_config["container_id"]
    checkbox_id = checkbox_config["checkbox_id"]
    type_name = checkbox_config["label_text"]

    # Assuming you have a function clean_filename defined elsewhere in your code
    folder_name = clean_filename(type_name)

    # Create a folder with the same name as the checkbox within the "checkbox" folder
    folder_path = os.path.join(type_folder, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Copy lopsliste.html to index.html in the folder
    shutil.copy2("../lopsliste.html", os.path.join(folder_path, "index.html"))

    # Replace the field containing the checkbox and add "active" or remove "active" accordingly
    with open(os.path.join(folder_path, "index.html"), 'r+', encoding='utf-8') as file:
        checkbox_container_id = checkbox_config["container_id"]
        checkbox_id = checkbox_config["checkbox_id"]
        label_text = checkbox_config["label_text"]
        content = file.read()
        for possible_checkbox in config["checkbox_mapping"]:
            
            # Trun off everyone else
            possible_checkbox_id = possible_checkbox["checkbox_id"]
            print(possible_checkbox_id)
            print(checkbox_id)

            possible_icon_class = checkbox_config["check_icon_class"]
            # Update the checkbox active status
            if checkbox_id == possible_checkbox_id:
                active_class = "active"
            else:
                active_class = ""

            string_to_replace = (
                f'<div id="{possible_checkbox_id}" class="header-checkbox active">'
            )

            string_to_replace_with = (
                f'<div id="{possible_checkbox_id}" class="header-checkbox {active_class}">'
            )

            content = content.replace(string_to_replace, string_to_replace_with)
        
        content = content.replace(config["title_find"], config["seo_category_title"] % type_name)
        content = content.replace(config["description"], config["seo_category_description"] % type_name)
        file.seek(0)
        file.write(content)
        file.truncate()
    
        # Generate sitemap string
    sitemap_string += f"<url>\n"
    sitemap_string += f"  <loc>https://lopskalender.com/category/{folder_name}/index.html</loc>\n"

    # Get the current date
    current_date = datetime.now().date()

    # Format the date as "YYYY-MM-DD"
    formatted_date = current_date.strftime("%Y-%m-%d")

    sitemap_string += f"  <lastmod>{formatted_date}T14:19:49+00:00</lastmod>\n"
    sitemap_string += f"  <priority>0.75</priority>\n"
    sitemap_string += f"</url>\n"


print("this can be used to insert into sitemap.xml")
print(sitemap_string)
