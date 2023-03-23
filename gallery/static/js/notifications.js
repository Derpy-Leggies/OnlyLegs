function addNotification(text='Sample notification', type=4) {
    let container = document.querySelector('.notifications');

    // Create notification element
    let div = document.createElement('div');
    div.classList.add('sniffle__notification');
    div.onclick = function() {
        if (div.parentNode) {
            div.classList.add('sniffle__notification--hide');

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
            div.classList.add('sniffle__notification--success');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M237.66,85.26l-128.4,128.4a8,8,0,0,1-11.32,0l-71.6-72a8,8,0,0,1,0-11.31l24-24a8,8,0,0,1,11.32,0l36.68,35.32a8,8,0,0,0,11.32,0l92.68-91.32a8,8,0,0,1,11.32,0l24,23.6A8,8,0,0,1,237.66,85.26Z" opacity="0.2"></path><path d="M243.28,68.24l-24-23.56a16,16,0,0,0-22.58,0L104,136h0l-.11-.11L67.25,100.62a16,16,0,0,0-22.57.06l-24,24a16,16,0,0,0,0,22.61l71.62,72a16,16,0,0,0,22.63,0L243.33,90.91A16,16,0,0,0,243.28,68.24ZM103.62,208,32,136l24-24,.11.11,36.64,35.27a16,16,0,0,0,22.52,0L208.06,56,232,79.6Z"></path></svg>';
            break;
        case 2:
            div.classList.add('sniffle__notification--error');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M215.46,216H40.54C27.92,216,20,202.79,26.13,192.09L113.59,40.22c6.3-11,22.52-11,28.82,0l87.46,151.87C236,202.79,228.08,216,215.46,216Z" opacity="0.2"></path><path d="M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z"></path></svg>';
            break;
        case 3:
            div.classList.add('sniffle__notification--warning');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M215.46,216H40.54C27.92,216,20,202.79,26.13,192.09L113.59,40.22c6.3-11,22.52-11,28.82,0l87.46,151.87C236,202.79,228.08,216,215.46,216Z" opacity="0.2"></path><path d="M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z"></path></svg>';
            break;
        default:
            div.classList.add('sniffle__notification--info');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a96,96,0,1,1-96-96A96,96,0,0,1,224,128Z" opacity="0.2"></path><path d="M144,176a8,8,0,0,1-8,8,16,16,0,0,1-16-16V128a8,8,0,0,1,0-16,16,16,0,0,1,16,16v40A8,8,0,0,1,144,176Zm88-48A104,104,0,1,1,128,24,104.11,104.11,0,0,1,232,128Zm-16,0a88,88,0,1,0-88,88A88.1,88.1,0,0,0,216,128ZM124,96a12,12,0,1,0-12-12A12,12,0,0,0,124,96Z"></path></svg>';
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
        div.classList.add('sniffle__notification-show');
    }, 100);

    // Remove notification after 5 seconds
    setTimeout(function() {
        if (div.parentNode) {
            div.classList.add('sniffle__notification--hide');

            setTimeout(function() {
                container.removeChild(div);
            }, 500);
        }
    }, 5000);
}