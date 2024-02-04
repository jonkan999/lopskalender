export function enlargeMarkersOnZoom(map) {
  // Define an object that maps zoom levels to class names
  const zoomClassMap = {
    6: "zoom-6",
    7: "zoom-7",
    8: "zoom-8",
    9: "zoom-9",
    10: "zoom-10",
    11: "zoom-11",
  };

  // Add a "zoomend" event listener to the map
  map.on("zoomend", function () {
    // Get the current zoom level
    const zoom = window.globalMap.getZoom();

    // Loop through the zoom levels in the class map
    for (const [zoomLevel, className] of Object.entries(zoomClassMap)) {
      const level = parseInt(zoomLevel);
      const markerClassList = `zoom-${level}`;

      // If the current zoom level is greater than or equal to the current
      // zoom level in the class map, add the class to all marker layers
      if (zoom >= level) {
        map.eachLayer(function (layer) {
          if (layer instanceof L.Marker) {
            layer._icon.classList.add(markerClassList);
          }
        });
      } else {
        // If the current zoom level is less than the current zoom level
        // in the class map, remove the class from all marker layers
        map.eachLayer(function (layer) {
          if (layer instanceof L.Marker) {
            layer._icon.classList.remove(markerClassList);
          }
        });
      }
    }
  });
}
