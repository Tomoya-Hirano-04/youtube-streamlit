document.addEventListener('DOMContentLoaded', function () {
    const propertyCards = document.querySelectorAll('.property-card');
    
    propertyCards.forEach(card => {
        card.addEventListener('click', function(event) {
            window.location = this.getAttribute('onclick').slice(11, -2); // Extract URL from 'linkClick' function
        });
    });
    
    const favButtons = document.querySelectorAll('.js-myListBtn216Image');
    
    favButtons.forEach(btn => {
        btn.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevent 'click' event on '.property-card'
            // Your function 'registClipSingle' here
            console.log('Favorite button clicked!');
        });
    });
});