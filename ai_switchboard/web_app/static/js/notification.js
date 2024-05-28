let latestNotificationTime = null;

function checkForNewNotification() {
    console.log("Checking for new notifications...");
    fetch('/latest_notification/')
        .then(response => response.json())
        .then(data => {
            if (data.message && (!latestNotificationTime || data.time_of_save > latestNotificationTime)) {
                latestNotificationTime = data.time_of_save;
                console.log("New Notifications...");

                let decrypted = data.message.split('|');

                let message = decrypted[0];

                let urls = [], file_names = [];
                for(let i = 1; i < decrypted.length; i++) {
                    let decryped_file = decrypted[i].split(',');
                    let file_id = decryped_file[0];
                    let file_name = decryped_file[1];
                    let data_format = decryped_file[2];
                    let url = `/download_file/${file_id}/${data_format}`;
                    urls.push(url);
                    file_names.push(file_name);
                }

                showNotificationPopup(message, file_names, urls);
            }
        });
}

function showNotificationPopup(message, files, urls) {
    // Create the popup
    let popup = document.createElement('div');
    popup.style.position = 'fixed';
    popup.style.left = '0';
    popup.style.right = '0';
    popup.style.top = '0';
    popup.style.bottom = '0';
    popup.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    popup.style.display = 'flex';
    popup.style.justifyContent = 'center';
    popup.style.alignItems = 'center';
    popup.style.zIndex = '1000';

    // Create the message box
    let messageBox = document.createElement('div');
    messageBox.style.backgroundColor = 'white';
    messageBox.style.padding = '20px';
    messageBox.style.borderRadius = '10px';
    messageBox.textContent = message;

    // Add the message box to the popup
    popup.appendChild(messageBox);

    // Add the popup to the body
    document.body.appendChild(popup);

    if(files.length > 0) {
        let downloadSection = document.createElement('div');
        downloadSection.style.marginTop = '10px';
        downloadSection.style.display = 'flex';
        downloadSection.style.flexDirection = 'column';
        downloadSection.style.alignItems = 'center';

        for(let i = 0; i < files.length; i++) {
            let downloadButton = document.createElement('a');
            downloadButton.href = urls[i];
            downloadButton.textContent = files[i];
            downloadButton.style.marginTop = '5px';
            downloadButton.style.padding = '5px 10px';
            downloadButton.style.backgroundColor = '#007bff';
            downloadButton.style.color = 'white';
            downloadButton.style.textDecoration = 'none';
            downloadButton.style.borderRadius = '5px';
            downloadButton.style.cursor = 'pointer';
            downloadButton.style.display = 'block';
            downloadButton.style.width = 'fit-content';
            downloadButton.style.textAlign = 'center';
            downloadButton.style.marginBottom = '5px';
            downloadSection.appendChild(downloadButton);
        }

        popup.appendChild(downloadSection);
    }

    // Remove the popup when clicked
    popup.addEventListener('click', () => {
        document.body.removeChild(popup);
    });
}

// Check for new notifications every 5 seconds
setInterval(checkForNewNotification, 5000);