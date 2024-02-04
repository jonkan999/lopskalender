var isFirstClick = true;

document.getElementById("preview").addEventListener("click", function () {
  if (isFirstClick) {
    var infoBox = document.querySelector(".race-info-box");
    var textBox = document.createElement("div");
    textBox.className = "nudge-text-box";
    textBox.textContent = "Klicka för att expandera";
    infoBox.appendChild(textBox);

    infoBox.addEventListener("click", function () {
      textBox.classList.add("hide");
      console.log("hide");
    });

    isFirstClick = false;
  }
});
