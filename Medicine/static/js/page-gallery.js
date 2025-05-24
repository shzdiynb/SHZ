/*---------- Gallery ----------*/
$(document).ready(function(){
 
    //MAGNIFIC-POPUP
    $(".page-gallery").magnificPopup({
        
        delegate: "a",
        type: "image",
        removalDelay: 500, //delay removal by X to allow out-animation
        gallery:{
            enabled: true
        },

    })


});