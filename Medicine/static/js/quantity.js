// Select all minus buttons
const minusButtons = document.querySelectorAll(".quantity .minus");

// Select all plus buttons
const plusButtons = document.querySelectorAll(".quantity .plus");

// Select all quantity input fields
const quantityInputs = document.querySelectorAll(".quantity .qty");

// Add click event listener to each minus button
minusButtons.forEach((button, index) => {
  button.addEventListener("click", () => {
    decreaseQuantity(index);
  });
});

// Add click event listener to each plus button
plusButtons.forEach((button, index) => {
  button.addEventListener("click", () => {
    increaseQuantity(index);
  });
});

// Function to decrease the quantity
function decreaseQuantity(index) {
  let currentQuantity = parseInt(quantityInputs[index].value);

  // Check if the current quantity is greater than 1
  if (currentQuantity > 1) {
    // Decrease the quantity by 1
    quantityInputs[index].value = currentQuantity - 1;
  }
} 

// Function to increase the quantity
function increaseQuantity(index) {
  let currentQuantity = parseInt(quantityInputs[index].value);

  // Check if the current quantity is less than 100
  if (currentQuantity < 100) {
    // Increase the quantity by 1
    quantityInputs[index].value = currentQuantity + 1;
  }
}