const previewButton = document.getElementById("preview");
const previewExitButton = document.getElementById("previewExit");
const addRaceForm = document.getElementById("addRaceForm");
const raceInfoBox = document.getElementById("raceInfoBox");
const dateElement = raceInfoBox.querySelector(".race-date");
const nameElement = raceInfoBox.querySelector(".race-name");
const typeElement = raceInfoBox.querySelector(".race-type-box");
const distanceElement = raceInfoBox.querySelector(".race-distance");
const websiteElement = raceInfoBox.querySelector(".race-website");
const summaryElement = raceInfoBox.querySelector(".race-info-summary-content");

/* Clicking in to preview view */
previewButton.addEventListener("click", function () {
  // Toggle the hide class on the addRaceForm and raceInfoBox elements
  addRaceForm.classList.toggle("hide");
  raceInfoBox.classList.toggle("hide");
  previewExitButton.classList.toggle("hide");

  var map = window.globalMap;

  if (map) {
    var existingMarker;

    map.eachLayer(function (layer) {
      if (layer instanceof L.Marker) {
        existingMarker = layer;
      }
    });
    console.log(existingMarker);
    if (existingMarker) {
      map.flyTo(existingMarker.getLatLng(), 13, {
        duration: 1, // adjust the duration as needed
      });
    }
  }

  // Populate the raceInfoBox with values from the form
  dateElement.textContent = document.getElementById("date").value;
  nameElement.textContent = document.getElementById("name").value;
  typeElement.innerHTML = `
                            <div class="text-icon-${
                              document.getElementById("type").value
                            }"></div>
                            <p class="race-type">${
                              document.getElementById("type").value
                            }</p>
  `;
  distanceElement.textContent = `Distanser: ${
    document.getElementById("distance").value
  }`;
  websiteElement.href = document.getElementById("website").value;
  summaryElement.textContent = document.getElementById("summary").value;
});
/* Clicking out of preview view */
previewExitButton.addEventListener("click", function () {
  if (raceInfoBox.classList.contains("race-info-box--expanded")) {
    raceInfoBox.classList.toggle("race-info-box--expanded");
    setTimeout(function () {
      // Toggle the hide class on the addRaceForm and raceInfoBox elements
      addRaceForm.classList.toggle("hide");
      raceInfoBox.classList.toggle("hide");
      previewExitButton.classList.toggle("hide");

      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth",
      });
    }, 200);
  } else {
    // Toggle the hide class on the addRaceForm and raceInfoBox elements
    addRaceForm.classList.toggle("hide");
    raceInfoBox.classList.toggle("hide");
    previewExitButton.classList.toggle("hide");

    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  }

  // Populate the raceInfoBox with values from the form
  /*   dateElement.textContent = document.getElementById("date").value;
  nameElement.textContent = document.getElementById("name").value;
  typeElement.textContent = document.getElementById("type").value;
  distanceElement.textContent = document.getElementById("distance").value;
  websiteElement.href = document.getElementById("website").value;
  summaryElement.textContent = document.getElementById("summary").value;  */
});
