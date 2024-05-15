/*!
* Start Bootstrap - Business Casual v7.0.9 (https://startbootstrap.com/theme/business-casual)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-casual/blob/master/LICENSE)
*/
// Highlights current date on contact page
window.addEventListener('DOMContentLoaded', event => {
    const listHoursArray = document.body.querySelectorAll('.list-hours li');
    listHoursArray[new Date().getDay()].classList.add(('today'));
})
document.body.addEventListener('click', function(event) {
    if (event.target && event.target.classList.contains('process-link')) {
        var selectedOption = document.getElementById('processing_model').value;
        var videoName = event.target.getAttribute('data-name');
        var urlTemplate = event.target.getAttribute('data-url-template');
        var url = urlTemplate.replace('placeholder_model', selectedOption).replace('placeholder_vid', videoName);
        event.target.setAttribute('href', url);
    }
});
