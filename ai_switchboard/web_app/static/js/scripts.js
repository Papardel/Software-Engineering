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
    if (event?.target.classList.contains('process-link')) {
        let selectedOption = document.getElementById('processing_model_display');
        let videoName = event.target.getAttribute('data-name');
        let url = `/process/${encodeURIComponent(videoName)}/${selectedOption.value}`;
        event.target.setAttribute('href', url);
    }
});

function deleteSelected(){
    let delete_all_selected = document.getElementById('delete_selected');

    let checkboxes = document.querySelectorAll('input[name="fileType"]:checked');
    let filters = Array.from(checkboxes).map(cb => cb.value.toLowerCase());
    let url_arg = filters.join('_');
    let url = `/delete_all_files/${url_arg}`;
    delete_all_selected.setAttribute('href', url);
}

function filterMedia() {
    let query = document.getElementById('searchBar').value.toLowerCase();
    let checkboxes = document.querySelectorAll('input[name="fileType"]:checked');
    let filters = Array.from(checkboxes).map(cb => cb.value.toLowerCase());

    let items = document.querySelectorAll('.media_file');
    items.forEach(item => {
        let itemName = item.querySelector('.file_name').textContent.toLowerCase();
        let itemFilter = item.getAttribute('data_type');
        let matchesQuery = itemName.includes(query);
        let matchesFilter = filters.length === 0 || filters.includes(itemFilter);

        if (matchesQuery && matchesFilter) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

function updateProcessMedia(){
    let format = document.getElementById('fileType').value;

    let model_select = document.getElementById('processing_model_display');
    let models = Array.from(model_select.options);
    let count = false;

    models.forEach(model => {
        let modelFormat = model.getAttribute('model_type');
        
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

    let search = document.getElementById('ProcessSearchBar').value.toLowerCase();
    let items = document.querySelectorAll('.processing_file');

    items.forEach(item => {
        let itemName = item.getAttribute('file_name');
        let itemType = item.getAttribute('file_type');
        let matchesQuery = itemName.includes(search);

        if (matchesQuery && itemType === format) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });

}