import { filterMarkersOnChecks } from "/js/filterMarkersOnChecks.js";
import { filterRaces } from "/js/filterRaces.js";

const relay = document.getElementById("relayCheckbox");
const terrain = document.getElementById("terrainCheckbox");
const trail = document.getElementById("trailCheckbox");
const road = document.getElementById("roadCheckbox");
const backyard = document.getElementById("backyardCheckbox");
const track = document.getElementById("trackCheckbox");

relay.addEventListener("click", function () {
  this.classList.toggle("active");
  /* If it was untoggled then it is toggled now */
  if (this.classList.contains("active")) {
    /* Was untoggled so after clicking we show */
    filterMarkersOnChecks("relay", "show");
    filterRaces();
  } else {
    filterMarkersOnChecks("relay", "hide");
    filterRaces();
  }
});
backyard.addEventListener("click", function () {
  this.classList.toggle("active");
  /* If it was untoggled then it is toggled now */
  if (this.classList.contains("active")) {
    /* Was untoggled so after clicking we show */
    filterMarkersOnChecks("backyard", "show");
    filterRaces();
  } else {
    filterMarkersOnChecks("backyard", "hide");
    filterRaces();
  }
});
terrain.addEventListener("click", function () {
  this.classList.toggle("active");
  if (this.classList.contains("active")) {
    filterMarkersOnChecks("terrain", "show");
    filterRaces();
  } else {
    filterMarkersOnChecks("terrain", "hide");
    filterRaces();
  }
});

trail.addEventListener("click", function () {
  this.classList.toggle("active");
  /* If it was untoggled then it is toggled now */
  if (this.classList.contains("active")) {
    /* Was untoggled so after clicking we show */
    filterMarkersOnChecks("trail", "show");
    filterRaces();
  } else {
    filterMarkersOnChecks("trail", "hide");
    filterRaces();
  }
});
road.addEventListener("click", function () {
  this.classList.toggle("active");
  if (this.classList.contains("active")) {
    filterMarkersOnChecks("road", "show");
    filterRaces();
  } else {
    filterMarkersOnChecks("road", "hide");
    filterRaces();
  }
});
track.addEventListener("click", function () {
  this.classList.toggle("active");
  if (this.classList.contains("active")) {
    filterMarkersOnChecks("track", "show");
    filterRaces();
  } else {
    filterMarkersOnChecks("track", "hide");
    filterRaces();
  }
});
