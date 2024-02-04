export function filterMarkersOnDistance(minDistance, maxDistance) {
  // Fetch all_races.json and parse it into a JavaScript object
  fetch("/all_races_w_formatted_summary.json")
    .then((response) => response.json())
    .then((allRaces) => {
      // Get all marker icons
      let markerIcons = document.getElementsByClassName("leaflet-marker-icon");

      // Loop through all marker icons and get all the distance_m arrays from allRaces
      for (let i = 0; i < markerIcons.length; i++) {
        // Get distance date from marker
        const distanceM = markerIcons[i]
          .querySelector("div")
          .getAttribute("data-marker-distance_m");
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
        if (
          distanceM === "backyard" ||
          distanceM === "time" ||
          distanceM === "relay"
        ) {
          /* if distanceM is "backyard" or "time" we show it independently of distance slider, such as backyard and time races */
          isInRange = true;
        }
        if (!isInRange) {
          // If none of the values in distance_m is between minDistance and maxDistance, add "hideMarkerOnDays" to markerIcons[i].classList
          markerIcons[i].classList.add("hideMarkerOnDistance");
        } else {
          // Otherwise, remove "hideMarkerOnDays" from markerIcons[i].classList
          markerIcons[i].classList.remove("hideMarkerOnDistance");
        }
      }
    })
    .catch((error) => console.error(error));
}
