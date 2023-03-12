function popUpShow(title, body, actions, content) {
    // Stop scrolling
    document.querySelector("html").style.overflow = "hidden";

    // Get popup elements
    var popup = document.querySelector('.pop-up');
    var popupContent = document.querySelector('.pop-up-content');
    var popupActions = document.querySelector('.pop-up-controlls');
    
    // Set popup content
    popupContent.innerHTML = `<h3>${title}</h3><p>${body}</p>${content}`;

    // Set buttons that will be displayed
    popupActions.innerHTML = actions;
    popupActions.innerHTML += '<button class="btn-block" onclick="popupDissmiss()">Nooooooo</button>';

    // Show popup
    popup.style.display = 'block';
    setTimeout(function() {
        popup.classList.add('active')
    }, 10);
}

function popupDissmiss() {
    // un-Stop scrolling
    document.querySelector("html").style.overflow = "auto";

    var popup = document.querySelector('.pop-up');

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