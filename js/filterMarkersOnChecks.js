export function filterMarkersOnChecks(type, action) {
  // Get all marker icons
  let markerIcons = document.getElementsByClassName("leaflet-marker-icon");
  const compareString = "marker-" + type;

  // Loop through all marker icons
  for (let i = 0; i < markerIcons.length; i++) {
    // Get the third class name
    let className = markerIcons[i].classList[1];

    if (compareString === className) {
      // If the marker class is the same type as input, we do
      if (action === "show") {
        // If action is show, we show. All icons are created with show marker on default
        markerIcons[i].classList.remove("hideMarkerOnCheck");
      } else {
        // If the marker date is not greater, remove the hideMarker class
        markerIcons[i].classList.add("hideMarkerOnCheck");
      }
    }
  }
}
