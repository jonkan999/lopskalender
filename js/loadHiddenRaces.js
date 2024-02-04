import { toggleBoxExpansion } from "/js/toggleBoxExpansion.js";

const container = document.querySelector(".race-container");
const months = [
  "Januari",
  "Februari",
  "Mars",
  "April",
  "Maj",
  "Juni",
  "Juli",
  "Augusti",
  "September",
  "Oktober",
  "November",
  "December",
];
let prevMonthYear = null;

// Load the JSON data
fetch("all_races_w_formatted_summary.json")
  .then((response) => response.json())
  .then((data) => {
    // Filter the data by date and distance

    // Create the race-info-boxes with display:none
    for (let race of data) {
      // Getting month name if its the first race occurance of the month
      const date = new Date(
        race.date.substring(0, 4),
        race.date.substring(4, 6) - 1,
        race.date.substring(6, 8)
      );
      const currentMonthYear = `${
        months[date.getMonth()]
      } ${date.getFullYear()}`;

      if (prevMonthYear !== currentMonthYear) {
        const monthName = document.createElement("div");
        monthName.classList.add("month-name");

        const monthHeader = document.createElement("h2");
        monthHeader.classList.add("secondary-header");
        monthHeader.style.marginBottom = "0.3rem";
        monthHeader.style.paddingLeft = "0.2rem";
        monthName.style.display = "none";
        monthHeader.textContent = currentMonthYear;
        monthName.appendChild(monthHeader);
        container.appendChild(monthName);
        prevMonthYear = currentMonthYear;
      }
      let div = document.createElement("div");
      div.classList.add("race-info-box");
      div.classList.add("margin-bottom--small");
      div.classList.add("border-style");
      div.style.display = "none";

      let upperDiv = document.createElement("div");
      upperDiv.classList.add("race-info-box-upper-content");

      if (race.name === "KfS Kungsholmen Runt") {
        div.classList.add("highlighted-box");
        let highlightText = document.createElement("div");
        highlightText.classList.add(`highlight-text-box-${race.type}`);
        highlightText.textContent = `featured ${race.type} race`;
        div.appendChild(highlightText);
      }

      let dateP = document.createElement("p");
      dateP.classList.add("race-date");

      // Convert YYYYMMDD string to Date object
      const year = race.date.substring(0, 4);
      const month = race.date.substring(4, 6);
      const day = race.date.substring(6, 8);

      //Convert to date
      const raceDate = new Date(`${year}-${month}-${day}`);
      let options = { day: "numeric", month: "short" };
      const raceDateString = raceDate.toLocaleDateString("sv-SE", options);
      dateP.textContent = `${raceDateString}`;

      let divText = document.createElement("div");
      divText.classList.add("race-text-box");
      divText.classList.add("margin-bottom--tiny");

      let nameP = document.createElement("h3");
      nameP.classList.add("race-name");
      nameP.classList.add("tertiary-header");

      nameP.textContent = `${race.name}`;

      let typeDiv = document.createElement("div");
      typeDiv.classList.add("race-type-box");
      typeDiv.classList.add("margin-bottom--tiny");

      let typeIcon = document.createElement("div");
      typeIcon.classList.add(`text-icon-${race.type}`);

      let typeP = document.createElement("p");
      typeP.classList.add("race-type");
      typeP.textContent = `${race.type}`;

      let distanceP = document.createElement("p");
      distanceP.classList.add("race-distance");

      let distance = race.distance_m;

      if (distance === "backyard") {
        distance = "Backyard Ultra";
      } else if (distance === "time") {
        distance = "Tidslopp";
      } else if (distance === "relay") {
        distance = "Stafett";
      } else if (Array.isArray(distance)) {
        distance = distance.map((d) => {
          if (d === "backyard") {
            return "Backyard Ultra";
          } else if (d === "time") {
            return "Tidslopp";
          } else if (d === "relay") {
            return "Stafett";
          } else if (race.type === "track") {
            return d;
          } else {
            return d / 1000;
          }
        });
        distance = distance.map((d) => {
          if (d >= 20.9 && d <= 21.3) {
            return "Halvmarathon";
          } else if (d >= 41.9 && d <= 42.4) {
            return "Marathon";
          } else if (typeof d === "number") {
            if (race.type === "track") {
              return d + " m";
            } else {
              return d + " km";
            }
          } else {
            return d;
          }
        });
        distance = distance.join(", ");
      } else {
        distance = distance / 1000;
        if (distance >= 20.9 && distance <= 21.3) {
          distance = "Halvmarathon";
        } else if (distance >= 41.9 && distance <= 42.4) {
          distance = "Marathon";
        } else {
          distance = distance + " km";
        }
      }

      distanceP.textContent = "" + distance;

      let websiteA = document.createElement("a");
      websiteA.classList.add("race-website");
      websiteA.href = race.website;
      websiteA.target = "_blank";

      websiteA.textContent = "Mer info";

      let summary = document.createElement("div");
      summary.classList.add("race-info-summary");
      let summaryP = document.createElement("p");
      summaryP.classList.add("race-info-summary-content");
      summaryP.innerHTML = `${race.summary}`;

      div.setAttribute("data-marker-id", race.id);
      /*           div.setAttribute(
        "data-marker-lat-long",
        `${race.latitude}, ${race.longitude}`
      );
      div.setAttribute("data-marker-distance_m", race.distance_m);
      div.setAttribute("data-marker-date", race.date);
      div.setAttribute("data-marker-type", race.type); */

      upperDiv.appendChild(dateP);
      upperDiv.appendChild(divText);
      divText.appendChild(nameP);
      divText.appendChild(typeDiv);
      typeDiv.appendChild(typeIcon);
      typeDiv.appendChild(typeP);

      divText.appendChild(distanceP);
      upperDiv.appendChild(websiteA);

      div.appendChild(upperDiv);

      summary.appendChild(summaryP);
      div.appendChild(summary);

      container.appendChild(div);

      /*Adding event listeners to the boxes*/
      const raceInfoBoxes = document.querySelectorAll(".race-info-box");
      raceInfoBoxes.forEach((raceInfoBox) => {
        raceInfoBox.addEventListener("click", toggleBoxExpansion);
      });
    }
  });
