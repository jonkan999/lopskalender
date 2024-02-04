export function filterMarkersOnDays(daysLow, daysHigh) {
  // Get all marker icons
  let markerIcons = document.getElementsByClassName("leaflet-marker-icon");

  fetch("/all_races_w_formatted_summary.json")
    /* Unneccessary fetch but serves the purpose of delaying this function 
    to after the initial document has finished loading. 
    This allows the initial filtering to run properly. Probably a better way of delaying*/
    .then((response) => response.json())
    .then((allRaces) => {
      // Loop through all marker icons
      for (let i = 0; i < markerIcons.length; i++) {
        // Get the third class name
        let className = markerIcons[i].classList[2];

        // Extract the date from the class name (assume it's the last 8 characters)
        let dateString = className.substring(className.length - 8);

        // Convert YYYYMMDD string to Date object
        const year = dateString.substring(0, 4);
        const month = dateString.substring(4, 6);
        const day = dateString.substring(6, 8);

        const raceDate = new Date(`${year}-${month}-${day}`);

        // Get current date
        const currentDate = new Date();
        // Calculate difference in milliseconds
        const diff = Math.max(raceDate - currentDate, 0);

        // Convert milliseconds to days
        const diffInDays = diff / (1000 * 60 * 60 * 24);

        // Compare the marker date to the current date
        if (diffInDays > daysLow && diffInDays < daysHigh) {
          //If diffInDays (between current date and scehduled race date)
          //is between slider dates, we remove the hide class and show marker
          markerIcons[i].classList.remove("hideMarkerOnDays");
        } else {
          // If the marker date is not greater, remove the hideMarker class
          markerIcons[i].classList.add("hideMarkerOnDays");
        }
      }
    })
    .catch((error) => console.error(error));
}
