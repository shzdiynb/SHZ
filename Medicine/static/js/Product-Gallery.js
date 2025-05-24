/*---------- Product Image Gallery ----------*/

// Get the main product image container and the main product image element
let productImage = document.querySelector(".product-des .image");
let productMain = document.querySelector(".main img");

// Get all the thumbnail images in the change-btns container
let productAll = document.querySelectorAll(".change-btns img");

// Add click event listeners to each thumbnail image
productAll.forEach(product => {

    product.addEventListener("click", () =>{

        /*----- Active Button -----*/
        productImage.querySelector(".active").classList.remove("active"); // Remove the "active" class from the currently active button
        product.classList.add("active"); // Add the "active" class to the clicked button to mark it as active

        /*----- Active Image -----*/
        let src = product.getAttribute("src"); // Get the source attribute of the clicked thumbnail image
        productMain.src = src; // Update the source attribute of the main product image to display the clicked image

    })
})