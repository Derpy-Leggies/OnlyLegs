function addNotification(notificationText, notificationLevel) {
    const notificationContainer = document.querySelector('.notifications');

    // Create notification element
    const notification = document.createElement('div');
    notification.classList.add('sniffle__notification');
    notification.onclick = () => {
        if (notification) {
            notification.classList.add('hide');

            setTimeout(() => {
                notificationContainer.removeChild(notification);
            }, 500);
        }
    };

    // Create icon element and append to notification
    const iconElement = document.createElement('span');
    iconElement.classList.add('sniffle__notification-icon');
    notification.appendChild(iconElement);
    
    // Set the icon based on the notification level, not pretty but it works :3
    if (notificationLevel === 1) {
        notification.classList.add('success');
        iconElement.innerHTML = '<i class="ph ph-check-circle"></i>';
    } else if (notificationLevel === 2) {
        notification.classList.add('critical');
        iconElement.innerHTML = '<i class="ph ph-warning"></i>';
    } else if (notificationLevel === 3) {
        notification.classList.add('warning');
        iconElement.innerHTML = '<i class="ph ph-siren"></i>';
    } else {
        notification.classList.add('info');
        iconElement.innerHTML = '<i class="ph ph-info"></i>';
    }

    // Create text element and append to notification
    const description = document.createElement('span');
    description.classList.add('sniffle__notification-text');
    description.innerHTML = notificationText;
    notification.appendChild(description);

    // Append notification to container
    notificationContainer.appendChild(notification);
    setTimeout(() => { notification.classList.add('show'); }, 5);

    // Remove notification after 5 seconds
    setTimeout(() => {
        if (notification) {
            notification.classList.add('hide');
            setTimeout(() => { 
                notificationContainer.removeChild(notification); 
            }, 500);
        }
    }, 5000);
}
