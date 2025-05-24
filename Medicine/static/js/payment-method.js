/*---------- Payment Methods ----------*/

// Wait for the document to be ready
$(document).ready(function () {
  // Add a click event listener to all labels inside the "payment" class
  $(".payment .radio-label").click(function () {
    // Remove the "active" class from all payment bodies
    $(".payment .payment-body").removeClass("active");
    
    // Add the "active" class to the next sibling with class "payment-body"
    $(this).next(".payment-body").addClass("active");
  });
});
