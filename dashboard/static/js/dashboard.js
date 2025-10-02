document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.querySelector(".btn-add");
  const grid = document.querySelector(".inventory-grid");

  if (addBtn && grid) {
    addBtn.addEventListener("click", () => {
      // Create a new inventory card
      const newCard = document.createElement("div");
      newCard.classList.add("inventory-card");

      // Card content
      newCard.innerHTML = `
        <h3>CREATED INVENTORY</h3>
        <p>New Inventory Item</p>
        <p>Details about this item...</p>
      `;

      // Add animation
      newCard.style.opacity = 0;
      grid.prepend(newCard); // Add card to the top of grid

      setTimeout(() => {
        newCard.style.transition = "opacity 0.4s ease-in";
        newCard.style.opacity = 1;
      }, 50);
    });
  }
});
