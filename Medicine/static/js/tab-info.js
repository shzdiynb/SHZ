/*---------- Tab Information ----------*/
// Select the tab buttons container.
var tabButtons = document.querySelector('.tab-info .tab-buttons');

// Add a click event listener to the tab buttons.
tabButtons.addEventListener('click', function (e) {

    // Check if the clicked element has the 'button' class and is not already active.
    if (e.target.classList.contains('button') && !e.target.classList.contains('active')) {

        var target = e.target.getAttribute('data-target'); // Get the target data attribute from the clicked button
        tabButtons.querySelector('.active').classList.remove('active'); // Remove the 'active' class from the currently active button
        e.target.classList.add('active'); // Add the 'active' class to the clicked button

        var tabSections = document.querySelector('.tab-info .tab-sections'); // Select the tab sections container.
        tabSections.querySelector('.tab-section.active').classList.remove('active'); // Remove the 'active' class from the currently active tab section
        tabSections.querySelector(target).classList.add('active'); // Add the 'active' class to the target section, making it visible.

    }

});
