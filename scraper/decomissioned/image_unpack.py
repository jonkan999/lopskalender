import base64
from PIL import Image
import io
from scraper_package import transform_module
import re

def save_webp_image(base64_data, output_path):
    # Decode the base64 data
    decoded_data = base64.b64decode(base64_data)

    # Open the image from the decoded data
    img = Image.open(io.BytesIO(decoded_data))

    # Save the image as a WebP file
    img.save(output_path, "WEBP", quality=85)


races = transform_module.import_json("transformed_races.json")

for race in races:
    print(race["name"])
    #for i,image in enumerate(race["contents"]["images"]):
    for i,image in enumerate(race["images"]):
        print(race["name"])
        if image:
            save_webp_image(image, f"images/{race['name'].replace('/', '-')}_{i}.webp")

