const hamburger = document.getElementById("hamburger");
const sidebar = document.getElementById("hamburger-sidebar");
const shadow = document.getElementById("body-shadow");

hamburger.addEventListener("click", () => {
  const isActive = sidebar.classList.toggle("active");
  shadow.style.display = sidebar.classList.contains("active")
    ? "block"
    : "none";
  document.body.classList.toggle("no-scroll", isActive);
});

window.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");
  const footer = document.querySelector("footer");

  document.documentElement.style.setProperty(
    "--header-height",
    header.offsetHeight + "px",
  );
  document.documentElement.style.setProperty(
    "--footer-height",
    footer.offsetHeight + "px",
  );
});
