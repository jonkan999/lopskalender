///////////////////////////////////////////////////////////
// Make mobile navigation work

const btnNavEl = document.querySelector(".btn-mobile-nav");
const headerEl = document.querySelector(".header-section");

btnNavEl.addEventListener("click", function () {
  headerEl.classList.toggle("nav-open");
  if (!headerEl.classList.contains("nav-open")) {
    //Opens leafelet controls
    // Get all elements with class "leaflet-control"
    /*     const elements = document.getElementsByClassName(
      "leaflet-control-container"
    );

    // Loop through all elements and set their display property to "none"
    for (let i = 0; i < elements.length; i++) {
      elements[i].style.display = "block";
    } */

    //This will run every time except the first
    setTimeout(function () {
      //removes nav-close after slide out effect
      headerEl.classList.toggle("nav-close");
    }, 500);
    headerEl.classList.toggle("nav-close");
  } else {
    //Closes leafelet controls
    // Get all elements with class "leaflet-control"
    /*     const elements = document.getElementsByClassName(
      "leaflet-control-container"
    );

    // Loop through all elements and set their display property to "none"
    for (let i = 0; i < elements.length; i++) {
      elements[i].style.display = "none";
    } */
  }
});
