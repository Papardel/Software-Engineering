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

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('processing_model_display')) {
        updateProcessMedia();
    }
});

document.body.addEventListener('click', function(event) {
    if (event.target && event.target.classList.contains('process-link')) {
        var selectedOption = document.getElementById('processing_model_display');
        var videoName = event.target.getAttribute('data-name');
        var url = `/process/${encodeURIComponent(videoName)}/${selectedOption.value}`;
        console.log(url);
        event.target.setAttribute('href', url);
    }
});

function filterMedia() {
    var query = document.getElementById('searchBar').value.toLowerCase();
    var checkboxes = document.querySelectorAll('input[name="fileType"]:checked');
    var filters = Array.from(checkboxes).map(cb => cb.value.toLowerCase());

    var items = document.querySelectorAll('.media_file');
    items.forEach(item => {
        var itemName = item.querySelector('.file_name').textContent.toLowerCase();
        var itemFilter = item.getAttribute('data_type');
        var matchesQuery = itemName.includes(query);
        var matchesFilter = filters.length === 0 || filters.includes(itemFilter);

        if (matchesQuery && matchesFilter) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

function updateProcessMedia(){
    var format = document.getElementById('fileType').value;

    var model_select = document.getElementById('processing_model_display');
    var models = Array.from(model_select.options);
    var count = false;

    models.forEach(model => {
        var modelFormat = model.getAttribute('model_type');
        
        if (modelFormat == format) {
            model.style.display = 'block';
            if (!count) {
                model.selected = true;
                count = true;
            }
        } else {
            model.style.display = 'none';
        }
    });

    var search = document.getElementById('ProcessSearchBar').value.toLowerCase();
    var items = document.querySelectorAll('.processing_file');

    items.forEach(item => {
        var itemName = item.getAttribute('file_name');
        var itemType = item.getAttribute('file_type');
        var matchesQuery = itemName.includes(search);

        if (matchesQuery && itemType === format) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });

}