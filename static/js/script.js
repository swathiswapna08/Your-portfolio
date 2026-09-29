document.addEventListener("DOMContentLoaded", () => {
  console.log("Your Portfolio Builder initialized.");

  // Smooth scroll for anchor links
  const navLinks = document.querySelectorAll(".nav-links a[href^='#']");
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      const targetId = link.getAttribute("href");
      if (targetId !== "#") {
        e.preventDefault();
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
          targetSection.scrollIntoView({ behavior: "smooth" });
        }
      }
    });
  });

  // Client-side validation check
  const portfolioForm = document.querySelector("form");
  if (portfolioForm) {
    portfolioForm.addEventListener("submit", (e) => {
      const nameInput = portfolioForm.querySelector("input[name='name']");
      if (nameInput && nameInput.value.trim() === "") {
        e.preventDefault();
        alert("Please enter your name before generating the portfolio.");
      }
    });
  }
});