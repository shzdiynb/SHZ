/*---------- Accordion ----------*/
// Document ready function to ensure the script runs after the DOM is fully loaded.
$(document).ready(function(){

  // Click event handler for the accordion.
  $(".accordion").click(function(){

    // Check if the clicked accordion is already active.
    if($(this).hasClass("active")){
      // If active, close the accordion by removing active class and changing the icon.
      $(this).removeClass("active");
      $(this).find("i").removeClass("fa-minus").addClass("fa-plus");
    }

    else{
      // If not active, close any open accordion and open the clicked one.
      $(".accordion").removeClass("active");
      $(".accordion .accordion-heading i").removeClass("fa-minus").addClass("fa-plus");
      $(this).addClass("active");
      $(this).find("i").removeClass("fa-plus").addClass("fa-minus");
    }
  })
})