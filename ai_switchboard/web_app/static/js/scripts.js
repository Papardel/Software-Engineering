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
        var selectedOption = document.getElementById('processing_model_display');
        var videoName = event.target.getAttribute('data-name');
        var url = `/process/${encodeURIComponent(videoName)}/${selectedOption.value}`;
        event.target.setAttribute('href', url);
    }
});

function UpdateProcessingContent(selectedFormat){
    $.ajax({
        url: '/update_process_content/',
        data: {'selected_format': selectedFormat},
        success: function(data) {
            var models = $('#processing_model_display');
            var media = $('#media_display');

            models.empty();
            $.each(data.models, function(index, item) {
                models.append('<option value="' + item + '">' + item + '</option>');
            });

            media.empty();
            $.each(data.media, function(index, item) {
                var media_item_format = '<a href="#" class="process-link" data-name="' + item + '">' + item + '</a>';
                media.append('<li class="list-unstyled list-hours mb-5 text-left mx-auto">'+media_item_format+'</li>');
            });
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}
function filterMedia() {
    var query = document.getElementById('searchBar').value.toLowerCase();
    var checkboxes = document.querySelectorAll('input[name="fileType"]:checked');
    var filters = Array.from(checkboxes).map(cb => cb.value.toLowerCase());

    var items = document.querySelectorAll('.media_file');
    items.forEach(item => {
        var itemName = item.querySelector('.file_name').textContent.toLowerCase();
        var itemFilter = item.getAttribute('data_type');
        console.log(itemFilter);
        var matchesQuery = itemName.includes(query);
        var matchesFilter = filters.length === 0 || filters.includes(itemFilter);

        if (matchesQuery && matchesFilter) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}