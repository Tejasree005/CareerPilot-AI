document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }
  document.querySelectorAll(".flash-close").forEach(button => {
    button.addEventListener("click", () => button.closest(".flash")?.remove());
  });
  document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener("change", () => {
      const box = input.closest(".upload-box");
      const file = input.files && input.files[0];
      if (box && file) {
        box.querySelector("strong").textContent = file.name;
        box.classList.add("file-selected");
      }
    });
  });
});
