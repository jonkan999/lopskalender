export async function loadCategoryMapping() {
  try {
    const response = await fetch(
      "/collection_configuration/general_config.yaml"
    );
    const yamlText = await response.text();
    const categoryMapping = jsyaml.load(yamlText);
    return [
      categoryMapping.category_mapping,
      categoryMapping.category_label_text,
    ];
  } catch (error) {
    console.error("Error loading category mapping:", error);
    return null;
  }
}

export async function filterRaces() {
  const button = document.querySelector(".toggle-button");

  if (button.classList.contains("active-button")) {
    // active button == list view

    // Get the values of the filters
    // Select all the checkboxes and store them in separate constants
    const trailCheckbox = document.querySelector("#trailCheckbox");
    const backyardCheckbox = document.querySelector("#backyardCheckbox");
    const terrainCheckbox = document.querySelector("#terrainCheckbox");
    const trackCheckbox = document.querySelector("#trackCheckbox");
    const roadCheckbox = document.querySelector("#roadCheckbox");
    const relayCheckbox = document.querySelector("#relayCheckbox");
    const countySelector = document.querySelector(".lan-filter-button");
    const categorySelector = document.querySelector(".category-filter-button");
    try {
      // Load the JSON data
      const response = await fetch("/all_races_w_formatted_summary.json");
      const data = await response.json();

      // Load category_mapping from YAML
      const categoryMappingObject = await loadCategoryMapping();
      const categoryMapping = categoryMappingObject[0];
      const categoryLabelText = categoryMappingObject[1];
      const filteredData = data.filter((race) => {
        let dateString = race.date;

        // Convert YYYYMMDD string to Date object
        const year = dateString.substring(0, 4);
        const month = dateString.substring(4, 6);
        const day = dateString.substring(6, 8);
        const power = 3;

        const raceDate = new Date(`${year}-${month}-${day}`);

        const daysLow = $("#sliderDays").slider("values", 0);
        const daysHigh = $("#sliderDays").slider("values", 1);
        let minDistance = Math.pow(
          $("#sliderDistance").slider("values", 0),
          power
        );
        let maxDistance = Math.pow(
          $("#sliderDistance").slider("values", 1),
          power
        );

        const currentDate = new Date();
        const diff = Math.max(raceDate - currentDate, 0);
        const diffInDays = Math.ceil(diff / (1000 * 3600 * 24));

        const distanceM = race.distance_m.toString();
        const distanceArr = distanceM.split(",").map((x) => parseInt(x));
        let isInRange = false;

        for (let j = 0; j < distanceArr.length; j++) {
          if (
            distanceArr[j] >= minDistance * 1000 &&
            distanceArr[j] <= maxDistance * 1000
          ) {
            isInRange = true;
            break;
          }
        }

        if (distanceM === "backyard" || distanceM === "relay") {
          isInRange = true;
        }

        let typeIsChecked = false;
        switch (race.type) {
          case "trail":
            if (trailCheckbox.classList.contains("active")) {
              typeIsChecked = true;
            }
            break;
          case "backyard":
            if (backyardCheckbox.classList.contains("active")) {
              typeIsChecked = true;
            }
            break;
          case "terrain":
            if (terrainCheckbox.classList.contains("active")) {
              typeIsChecked = true;
            }
            break;
          case "track":
            if (trackCheckbox.classList.contains("active")) {
              typeIsChecked = true;
            }
            break;
          case "road":
            if (roadCheckbox.classList.contains("active")) {
              typeIsChecked = true;
            }
            break;
          case "relay":
            if (relayCheckbox.classList.contains("active")) {
              typeIsChecked = true;
            }
            break;
        }

        let isCounty = false;
        const selectedValue = countySelector.value;
        console.log(selectedValue);

        if (selectedValue) {
          if (selectedValue === "Alla län") {
            isCounty = true;
          } else {
            const raceCounty = race.county;
            if (raceCounty) {
              isCounty = raceCounty === selectedValue;
            }
          }
        } else {
          isCounty = true;
        }

        let categoryIsChecked = false;
        const selectedCategory = categorySelector.value;
        // Check if the selected category is the default value
        if (categoryMapping[selectedCategory] === undefined) {
          categoryIsChecked = true;
        }
        // Check if the selected category exists in categoryMapping
        else if (categoryMapping[selectedCategory]) {
          // If a distance category is selected, ignore distance slider and set it to min/max:
          // Set isInRange to true
          isInRange = true;

          // Set slider distance handles to minimum and maximum values
          $("#sliderDistance").slider(
            "values",
            0,
            $("#sliderDistance").slider("option", "min")
          );
          $("#sliderDistance").slider(
            "values",
            1,
            $("#sliderDistance").slider("option", "max")
          );

          // Access properties of the category from categoryMapping
          const categoryData = categoryMapping[selectedCategory];

          if (Array.isArray(categoryData.range)) {
            const [minDistance, maxDistance] = categoryData.range;
            if (
              distanceArr.some(
                (distance) =>
                  distance >= minDistance * 1000 &&
                  distance <= maxDistance * 1000
              )
            ) {
              categoryIsChecked = true;
            }
          } else {
            if (distanceM.includes(categoryData)) {
              categoryIsChecked = true;
            }
          }
        }

        return (
          isCounty &&
          isInRange &&
          typeIsChecked &&
          diffInDays > daysLow &&
          diffInDays < daysHigh &&
          categoryIsChecked
        );
      });

      //Turn off all months each time, maybe a more efficient way of doing this?
      const monthNames = document.querySelectorAll(".month-name");
      monthNames.forEach((monthName) => {
        monthName.style.display = "none";
      });

      // Select all elements with the class "race-info-box"
      const raceInfoBoxes = document.querySelectorAll(".race-info-box");

      // Iterate through each race-info-box element
      raceInfoBoxes.forEach((raceInfoBox) => {
        // Get the value of the data-marker-id attribute
        const dataMarkerId = raceInfoBox.getAttribute("data-marker-id");
        // Find the matching race object in filteredData
        const race = filteredData.find((r) => r.id === dataMarkerId);
        // If the race object does not exist, hide the element
        if (!race) {
          raceInfoBox.style.display = "none";
        }
        // If the race object exists, show the element and check for nearest month name sibling and turn it on
        else {
          raceInfoBox.style.display = "block";
          const monthNameSibling = getNearestMonthNameSibling(raceInfoBox);
          if (monthNameSibling && monthNameSibling.style.display === "none") {
            monthNameSibling.style.display = "block";
          }
        }
      });
    } catch (error) {
      console.error("Error fetching or processing data:", error);
    }
  }
}

function getNearestMonthNameSibling(element) {
  let sibling = element.previousElementSibling;
  while (sibling) {
    if (sibling.classList.contains("month-name")) {
      return sibling;
    }
    sibling = sibling.previousElementSibling;
  }
  return null;
}
