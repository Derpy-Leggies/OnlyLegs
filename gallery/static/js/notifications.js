function addNotification(text='Sample notification', type=4) {
    let container = document.querySelector('.notifications');

    // Create notification element
    let div = document.createElement('div');
    div.classList.add('sniffle__notification');
    div.onclick = function() {
        if (div.parentNode) {
            div.classList.add('hide');

            setTimeout(function() {
                container.removeChild(div);
            }, 500);
        }
    };

    // Create icon element and append to notification
    let icon = document.createElement('span');
    icon.classList.add('sniffle__notification-icon');
    switch (type) {
        case 1:
            div.classList.add('success');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M229.66,77.66l-128,128a8,8,0,0,1-11.32,0l-56-56a8,8,0,0,1,11.32-11.32L96,188.69,218.34,66.34a8,8,0,0,1,11.32,11.32Z"></path></svg>';
            break;
        case 2:
            div.classList.add('critical');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z"></path></svg>';
            break;
        case 3:
            div.classList.add('warning');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z"></path></svg>';
            break;
        default:
            div.classList.add('info');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm16-40a8,8,0,0,1-8,8,16,16,0,0,1-16-16V128a8,8,0,0,1,0-16,16,16,0,0,1,16,16v40A8,8,0,0,1,144,176ZM112,84a12,12,0,1,1,12,12A12,12,0,0,1,112,84Z"></path></svg>';
            break;
    }
    div.appendChild(icon);

    // Create text element and append to notification
    let description = document.createElement('span');
    description.classList.add('sniffle__notification-text');
    description.innerHTML = text;
    div.appendChild(description);

    // Create span to show time remaining
    let timer = document.createElement('span');
    timer.classList.add('sniffle__notification-time');
    div.appendChild(timer);

    // Append notification to container
    container.appendChild(div);
    setTimeout(function() {
        div.classList.add('show');
    }, 100);

    // Remove notification after 5 seconds
    setTimeout(function() {
        if (div.parentNode) {
            div.classList.add('hide');

            setTimeout(function() {
                container.removeChild(div);
            }, 500);
        }
    }, 5000);
}