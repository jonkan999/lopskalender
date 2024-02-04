export function toggleBoxExpansion(event) {
  const raceInfoBox = event.currentTarget;
  const summaryDiv = raceInfoBox.querySelector(".race-info-summary");
  const currentPosition = window.pageYOffset;

  raceInfoBox.classList.toggle("race-info-box--expanded");
  summaryDiv.classList.toggle("show-div");
}
