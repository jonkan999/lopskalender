// Replace "YOUR_MAPBOX_ACCESS_TOKEN" with your actual Mapbox access token
mapboxgl.accessToken =
  "pk.eyJ1Ijoiam9ua2FueDMiLCJhIjoiY2xsdHRyNDU2MHUxYTNlbzdzZHB2aGkyZiJ9._hS--VA8nG49uiiDGpBK3w";

// Assuming you already have the mapboxgl library loaded and the HTML structure in place
// Access the existing map container element
const mapContainer = document.getElementById("mapboxContainer");

// Get the mapboxCenter from the data attribute
const mapboxCenter = JSON.parse(mapContainer.getAttribute("data-mapboxCenter"));

// Create a DOM element for the custom marker
function createMarkerElement(svg) {
  const markerElement = document.createElement("div");
  markerElement.innerHTML = svg;
  return markerElement;
}

// Custom marker SVG
const markerSvg = `
    <svg display="block" height="41px" width="27px" viewBox="0 0 27 41">
        <!-- ... other SVG elements ... -->
        <g transform="translate(8.0, 8.0)">
            <circle fill="#9c51b6" opacity="0.25" cx="5.5" cy="5.5" r="5.4999962"></circle>
            <circle fill="#9c51b6" cx="5.5" cy="5.5" r="5.4999962"></circle>
        </g>
    </svg>`;

// Initialize the map and center it on the obtained coordinates
const map = new mapboxgl.Map({
  container: mapContainer,
  style: "mapbox://styles/mapbox/light-v10",
  center: mapboxCenter,
  zoom: 11,
});

// Add a custom marker at the center coordinates
new mapboxgl.Marker({ element: createMarkerElement(markerSvg) })
  .setLngLat(mapboxCenter)
  .addTo(map);

map.on("load", () => {
  // Remove the Mapbox logo element
  const mapboxLogo = document.querySelector(".mapboxgl-ctrl-logo");
  if (mapboxLogo) {
    mapboxLogo.parentNode.removeChild(mapboxLogo);
  }

  // Remove the "Improve this map" link element
  const improveMapLink = document.querySelector(".mapbox-improve-map");
  if (improveMapLink) {
    improveMapLink.parentNode.removeChild(improveMapLink);
  }
});

/* SHOW ALL IMAGES */

document.getElementById("showAll").addEventListener("click", function () {
  // Show overlay
  document.getElementById("showAllOverlay").style.display = "block";
  document.getElementById("hideGrid").style.display = "flex";

  // Hide 'imageSection'
  /*  document.getElementById("imageSection").style.display = "none"; */

  // Show 'showAllGrid'
  document.getElementById("showAllGrid").style.display = "grid";

  // Smooth scroll to the top
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

document.getElementById("hideGrid").addEventListener("click", function () {
  // Show overlay
  document.getElementById("showAllOverlay").style.display = "none";
  document.getElementById("hideGrid").style.display = "none";

  // Hide 'imageSection'
  /*  document.getElementById("imageSection").style.display = "none"; */

  // Show 'showAllGrid'
  document.getElementById("showAllGrid").style.display = "none";
});
