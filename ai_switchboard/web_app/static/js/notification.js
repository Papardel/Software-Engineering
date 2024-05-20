let latestNotificationTime = null;

function checkForNewNotification() {
    console.log("Checking for new notifications...")
    fetch('/latest_notification/')
        .then(response => response.json())
        .then(data => {
            if (data.message && (!latestNotificationTime || data.time_of_save > latestNotificationTime)) {
                latestNotificationTime = data.time_of_save;
                console.log("New Notifications...")
                showNotificationPopup(data.message);
            }
        });
}

function showNotificationPopup(message) {
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

    // Remove the popup when clicked
    popup.addEventListener('click', () => {
        document.body.removeChild(popup);
    });
}

// Check for new notifications every 5 seconds
setInterval(checkForNewNotification, 5000);