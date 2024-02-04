import { filterMarkersOnDays } from "/js/filterMarkersOnDays.js";
import { filterRaces } from "/js/filterRaces.js";

$(function () {
  $("#sliderDays").slider({
    range: true,
    min: 0,
    max: 340,
    values: [0, 340],
    slide: function (event, ui) {
      let now = new Date();
      let dayInMilliseconds = 24 * 60 * 60 * 1000;
      let startDay = $("#sliderDays").slider("values", 0);
      let endDay = $("#sliderDays").slider("values", 1);
      let startDate = new Date(now.getTime() + startDay * dayInMilliseconds);
      let endDate = new Date(now.getTime() + endDay * dayInMilliseconds);

      let options = { day: "numeric", month: "short" };
      let startDateString = startDate.toLocaleDateString("sv-SE", options);
      let endDateString = endDate.toLocaleDateString("sv-SE", options);

      $("#daysFilterText").val(startDateString + " - " + endDateString);

      // Use the startDay and endDay values for the downstream function
      filterMarkersOnDays(startDay, endDay);
      const button = document.querySelector(".view-button.list-view-button");
      filterRaces();
    },
  });
  let now = new Date();
  let dayInMilliseconds = 24 * 60 * 60 * 1000;
  let startDate = new Date(
    now.getTime() + $("#sliderDays").slider("values", 0) * dayInMilliseconds
  );
  let endDate = new Date(
    now.getTime() + $("#sliderDays").slider("values", 1) * dayInMilliseconds
  );

  let startDay = $("#sliderDays").slider("values", 0);
  let endDay = $("#sliderDays").slider("values", 1);

  let options = { day: "numeric", month: "short" };
  let startDateString = startDate.toLocaleDateString("sv-SE", options);
  let endDateString = endDate.toLocaleDateString("sv-SE", options);

  $("#daysFilterText").val(startDateString + " - " + endDateString);
  // Add touch support
  $("#sliderDays").draggable();
  $("#sliderDays .ui-slider-handle").on("touchstart mousedown", function () {
    // Trigger the slider handle's mouseenter event
    $(this).trigger("mouseenter");
  });

  filterMarkersOnDays(startDay, endDay);
  console.log(startDay + ", " + endDay);
});
