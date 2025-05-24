/*---------- Counter-Up ----------*/

$(document).ready(function(){

  // Loop through each element with class 'count'
  $('.count').each(function() {

    var $this = $(this),
      countTo = $this.attr('data-count'); // Get the target value
    
    // Animate the counting from the 'Current Value' to the 'Target Value'
    $({ countNum: $this.text()}).animate({
      countNum: countTo // Animate towards the target value
    },
    {
      duration: 5000, // Animation duration (5 seconds)

      // Function called on each step of the animation
      step: function() {
        $this.text(Math.floor(this.countNum)); // Update the displayed value
      }, 

      // Function called when the animation is complete
      complete: function() {
        $this.text(this.countNum + '+'); // Update the displayed value with a '+' sign
      }
    });
  });
  
});