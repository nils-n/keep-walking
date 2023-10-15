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
