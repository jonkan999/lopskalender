import { toggleBoxExpansion } from "/js/toggleBoxExpansion.js";
import { enlargeMarkersOnZoom } from "/js/enlargeMarkersOnZoom.js";

// Create a map centered on a specific location
let map = L.map("map", { attributionControl: false }).setView(
  [59.346972, 15.748689],
  6
);
window.globalMap = map;

let MAPBOX_API_KEY = "";

// Fetching mapbox API
fetch(
  "/.netlify/functions/get-api-key"
  /* "/backend/config.json" */
)
  .then((response) => response.json())
  .then((data) => {
    const MAPBOX_API_KEY = data.MAPBOX_BASIC_STYLE_API_KEY;
    // Add a tile layer to the map
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/jonkanx3/cleil8zxx001201o9krzob8a5/tiles/{z}/{x}/{y}?access_token=" +
        MAPBOX_API_KEY,
      {
        minZoom: 5,
        maxZoom: 19,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }
    ).addTo(map);
  })
  .catch((error) => {
    console.error("Error loading config file", error);
  });

let marker;

// Add an event listener to the map that creates a marker on a click
map.on("click", function (event) {
  if (marker) {
    marker.remove();
  }
  const markerClass = document.getElementById("type").value || "default";
  const latlng = event.latlng;
  console.log("clicked");
  marker = L.marker(latlng, {
    icon: new L.DivIcon({
      className: `marker-${markerClass}`,
      iconSize: [12, 12],
    }),
  }).addTo(map);

  // Set the value of the latitude and longitude inputs, and update text in display box
  document.getElementById("latitude").value = latlng.lat;
  document.getElementById("longitude").value = latlng.lng;
  document.getElementById(
    "latlongBox"
  ).innerHTML = `Loppets latitud: ${latlng.lat.toFixed(
    2
  )} och longitud: ${latlng.lng.toFixed(2)}`;
});

// Update marker class when type select value changes
const typeSelect = document.getElementById("type");
typeSelect.addEventListener("change", function () {
  if (marker) {
    const markerClass = typeSelect.value || "default";
    marker.getElement().className = `marker marker-${markerClass}`;
  }
});

const raceInfoBoxes = document.querySelectorAll(".race-info-box");
raceInfoBoxes.forEach((raceInfoBox) => {
  raceInfoBox.addEventListener("click", toggleBoxExpansion);
});

/* Adding functionality for enlarging markers on zoom */
enlargeMarkersOnZoom(map);
