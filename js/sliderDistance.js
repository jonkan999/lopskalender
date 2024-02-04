import { filterMarkersOnDistance } from "/js/filterMarkersOnDistance.js";
/* import { initialFilter } from "/js/initialFilter.js"; */
import { filterRaces } from "/js/filterRaces.js";

const power = 3;

$(function () {
  $("#sliderDistance").slider({
    range: true,
    min: 0,
    max: 6,
    step: 0.1,
    values: [1.8, 2.5],
    slide: function (event, ui) {
      let minDistance = Math.pow(ui.values[0], power);
      let maxDistance = Math.pow(ui.values[1], power);

      // Round the distance values to the nearest integer
      minDistance = Math.round(minDistance);
      maxDistance = Math.round(maxDistance);

      $("#distanceFilterText").val(minDistance + " - " + maxDistance + "km");

      // Reset categorySelector.value to its default
      const categorySelector = document.querySelector(
        ".category-filter-button"
      );
      categorySelector.value = ""; // Set to the default value, adjust as needed

      filterMarkersOnDistance(minDistance, maxDistance);
      filterRaces();
    },
  });

  let minDistance = Math.pow($("#sliderDistance").slider("values", 0), power);
  let maxDistance = Math.pow($("#sliderDistance").slider("values", 1), power);

  // Round the distance values to the nearest integer
  minDistance = Math.round(minDistance);
  maxDistance = Math.round(maxDistance);

  filterMarkersOnDistance(minDistance, maxDistance);
  $("#distanceFilterText").val(minDistance + " - " + maxDistance + "km");
  // Add touch support
  $("#sliderDistance").draggable();
  $("#sliderDistance .ui-slider-handle").on(
    "touchstart mousedown",
    function () {
      // Trigger the slider handle's mouseenter event

      // Reset categorySelector.value to its default
      const categorySelector = document.querySelector(
        ".category-filter-button"
      );
      categorySelector.value = ""; // Set to the default value, adjust as needed

      $(this).trigger("mouseenter");
    }
  );

  /* initialFilter(); */
});
