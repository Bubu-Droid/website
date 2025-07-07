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

      // heading.appendChild(anchor);
      heading.insertBefore(anchor, heading.firstChild);
    });
});
