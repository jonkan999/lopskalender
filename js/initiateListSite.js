import { filterRaces } from "/js/filterRaces.js";
filterRaces();

//Fix som padding and margins
// If the window size is narrower than 704px, apply the media query style
const checkboxes = document.querySelector(".checkboxes");

const filterSection = document.querySelector(".filter-section");
const mapViewButton = document.querySelector(".map-view-button");
// Check if the window size is narrower than 704px
const mediaQuery = window.matchMedia("(max-width: 704px)");
if (mediaQuery.matches) {
  // Your media query style here
  filterSection.style.marginTop = "6rem";
  checkboxes.style.marginTop = "-4rem";
  /* mapViewButton.style.width = "8rem"; */
} else {
  filterSection.style.marginTop = "3rem";
  /* mapViewButton.style.width = "8rem"; */
}
// add county filter
const countySelector = document.getElementById("county-selector");
countySelector.style.display = "block";
setTimeout(function () {
  countySelector.style.opacity = "1";
}, 10);
// add category filter
const categorySelector = document.getElementById("category-selector");
categorySelector.style.display = "block";
setTimeout(function () {
  categorySelector.style.opacity = "1";
}, 10);

const element = document.querySelector(".map-or-list-view");

countySelector.addEventListener("change", function () {
  filterRaces();
});

categorySelector.addEventListener("change", function () {
  filterRaces();
});
