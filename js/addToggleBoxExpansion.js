import { toggleBoxExpansion } from "/js/toggleBoxExpansion.js";

const raceInfoBoxes = document.querySelectorAll(".race-info-box");
raceInfoBoxes.forEach((raceInfoBox) => {
  raceInfoBox.addEventListener("click", toggleBoxExpansion);
});
