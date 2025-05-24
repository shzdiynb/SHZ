/*--------------- Home Slider ---------------*/ 
var swiper = new Swiper(".home-slider", {

  loop:true, // Enable looping of slides
  
  autoplay: {
    delay: 5000, // Delay between slide transitions
    disableOnInteraction: false, // Allow autoplay on user interaction
  },

  pagination: {
    el: ".swiper-pagination1", // Pagination element
    clickable: true, // Enable clickable pagination bullets
  },

  navigation: {
    nextEl: ".swiper-button-next", // Next slide button
    prevEl: ".swiper-button-prev", // Previous slide button
  },

}); 