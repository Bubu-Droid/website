// Set up hamburger interaction
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

document.addEventListener("click", (event) => {
  const clickedInsideSidebar = sidebar.contains(event.target);
  const clickedOnHamburger = hamburger.contains(event.target);

  const isSidebarActive = sidebar.classList.contains("active");

  if (isSidebarActive && !clickedInsideSidebar && !clickedOnHamburger) {
    sidebar.classList.remove("active");
    shadow.style.display = "none";
    document.body.classList.remove("no-scroll");
  }
});

// Set position of header and footer
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

// Set up header anchoring for linked headings
document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(
      "h1.anchored, h2.anchored, h3.anchored, h4.anchored, h5.anchored, h6.anchored",
    )
    .forEach(function (heading) {
      if (!heading.id) return;

      const anchor = document.createElement("a");
      anchor.href = `#${heading.id}`;
      anchor.className = "heading-anchor";
      anchor.setAttribute("aria-label", "Anchor link to this section");
      anchor.innerHTML = "🔗";

      heading.appendChild(anchor);
      // heading.insertBefore(anchor, heading.firstChild);
    });
});

// Set up scroll to top button interaction
const scrollBtn = document.getElementById("scroll-to-top-btn");

window.addEventListener("scroll", () => {
  if (window.scrollY > 200) {
    scrollBtn.classList.add("show");
  } else {
    scrollBtn.classList.remove("show");
  }
});

scrollBtn.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

// Set up display math squishing for narrow width
// function scaleOverflowingMath() {
//   document.querySelectorAll(".MathJax[display=true]").forEach((mjx) => {
//     let wrapper = mjx.parentElement;
//
//     if (!wrapper.classList.contains("mjx-wrapper")) {
//       const w = document.createElement("span");
//       w.className = "mjx-wrapper";
//       mjx.replaceWith(w);
//       w.appendChild(mjx);
//       wrapper = w;
//     }
//
//     // reset
//     mjx.style.transform = "";
//     wrapper.classList.remove("scaled");
//
//     const mathWidth = mjx.scrollWidth;
//     const containerWidth = wrapper.clientWidth;
//
//     if (mathWidth > containerWidth && containerWidth > 0) {
//       const scaleX = containerWidth / mathWidth;
//       mjx.style.transform = `scaleX(${scaleX})`;
//       wrapper.classList.add("scaled");
//     }
//   });
// }
