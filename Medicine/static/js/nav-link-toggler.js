/*---------- Mobile-Navbar Nav Toggler ----------*/
$(document).ready(function(){
  
  // Handle main navigation link clicking
  $(".main-nav-link").click(function(){

    // Check if the clicked link is already active
    if($(this).hasClass("active")){
      $(this).removeClass("active"); // Remove "active" class from clicked link
      $(this).next(".sub-nav-link").removeClass("active").slideUp(); // Remove "active" class and slide up the corresponding sub-navigation
      $(this).find("i").removeClass("fa-minus").addClass("fa-plus"); // Update the icon to "fa-plus"
    }
    
    else{
      $(".nav-link .main-nav-link").removeClass("active"); // Remove "active" class from all main navigation links
      $(".nav-link .sub-nav-link").removeClass("active").slideUp(); // Remove "active" class and slide up all sub-navigations
      $(".nav-link .main-nav-link i").removeClass("fa-minus").addClass("fa-plus"); // Update all icons to "fa-plus"
      $(this).addClass("active"); // Add "active" class to clicked link
      $(this).next(".sub-nav-link").addClass("active").slideDown(); // Add "active" class and slide down the corresponding sub-navigation
      $(this).find("i").removeClass("fa-plus").addClass("fa-minus"); // Update the icon to "fa-minus"
    }

  });
  
});