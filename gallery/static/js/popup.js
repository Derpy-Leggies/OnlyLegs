function popUpShow(title, body, actions = '<button class="btn-block" onclick="popupDissmiss()">Close</button>', content = '') {
    // Stop scrolling
    document.querySelector("html").style.overflow = "hidden";

    // Get popup elements
    let popup = document.querySelector('.pop-up');
    let popupContent = document.querySelector('.pop-up-content');
    let popupActions = document.querySelector('.pop-up-controlls');
    
    // Set popup content
    popupContent.innerHTML = `<h3>${title}</h3><p>${body}</p>${content}`;

    // Set buttons that will be displayed
    popupActions.innerHTML = actions;

    // Show popup
    popup.style.display = 'block';
    setTimeout(function() {
        popup.classList.add('active')
    }, 10);
}

function popupDissmiss() {
    // un-Stop scrolling
    document.querySelector("html").style.overflow = "auto";

    let popup = document.querySelector('.pop-up');

    popup.classList.remove('active');

    setTimeout(function() {
        popup.style.display = 'none';
    }, 200);
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        if (document.querySelector('.pop-up').classList.contains('active')) {
            popupDissmiss();
        }
    }
});