console.log("well well well");

//toggle hamburger button when clicked on navbar
const navButton = document.getElementById("hamburger-button");
navButton.addEventListener("click", (e) => {
  hamburgerIcon = document.getElementById("hamburger-nav");
  crossIcon = document.getElementById("cross-nav");
  navLinks = document.getElementById("nav-links");

  if (hamburgerIcon.classList.contains("hidden")) {
    hamburgerIcon.classList.remove("hidden");
    crossIcon.classList.add("hidden");
    navLinks.classList.add("hidden");
  } else {
    hamburgerIcon.classList.add("hidden");
    crossIcon.classList.remove("hidden");
    navLinks.classList.remove("hidden");
  }
});

//to make messages disappear after fading out
const message = document.getElementById("message-list");
message.addEventListener("animationend", function () {
  message.style.opacity = 0;
  message.style.visibility = "hidden";
});
message.addEventListener("animationstart", function () {
  message.style.opacity = 1;
  message.style.visibility = "visible";
});
