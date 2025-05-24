const rangeInput = document.querySelectorAll(".range-input input"), // Get all range input elements
priceInput = document.querySelectorAll(".price-input input"), // Get all price input elements
range = document.querySelector(".slider .progress"); // Get the range element for displaying the progress
let priceGap = 100; // Define the desired price gap

// Event listeners for price inputs
priceInput.forEach(input => {
  input.addEventListener("input", e => {
    let minPrice = parseInt(priceInput[0].value), // Get the minimum price value
      maxPrice = parseInt(priceInput[1].value); // Get the maximum price value

    // Check if the price gap is within the desired range and the maxPrice is within the allowed range
    if ((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max) {
      if (e.target.className === "input-min") {
        rangeInput[0].value = minPrice; // Update the range input value for the minimum price
        range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%"; // Update the range progress position
      } else {
        rangeInput[1].value = maxPrice; // Update the range input value for the maximum price
        range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%"; // Update the range progress position
      }
    }
  });
});

// Event listeners for range inputs
rangeInput.forEach(input => {
  input.addEventListener("input", e => {
    let minVal = parseInt(rangeInput[0].value), // Get the minimum range value
      maxVal = parseInt(rangeInput[1].value); // Get the maximum range value

    // Check if the price gap is smaller than the desired range
    if ((maxVal - minVal) < priceGap) {
      if (e.target.className === "range-min") {
        rangeInput[0].value = maxVal - priceGap; // Adjust the minimum range value to maintain the price gap
      } else {
        rangeInput[1].value = minVal + priceGap; // Adjust the maximum range value to maintain the price gap
      }
    } else {
      priceInput[0].value = minVal; // Update the minimum price input value
      priceInput[1].value = maxVal; // Update the maximum price input value
      range.style.left = ((minVal / rangeInput[0].max) * 100) + "%"; // Update the range progress position for the minimum value
      range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%"; // Update the range progress position for the maximum value
    }
  });
});