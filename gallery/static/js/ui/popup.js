function popUpShow(title, body, actions, content) {
    // Stop scrolling
    document.querySelector("html").style.overflow = "hidden";

    var popup = document.querySelector('.pop-up');
    var popupContent = document.querySelector('.pop-up-content');
    var popupActions = document.querySelector('.pop-up-controlls');

    // Set tile and description
    h3 = document.createElement('h3');
    h3.innerHTML = title;
    p = document.createElement('p');
    p.innerHTML = body;

    popupContent.innerHTML = '';
    popupContent.appendChild(h3);
    popupContent.appendChild(p);

    // Set content
    if (content != '') {
        popupContent.innerHTML += content;
    }

    // Set buttons that will be displayed
    popupActions.innerHTML = '';
    if (actions != '') {
        popupActions.innerHTML += actions;
    }
    popupActions.innerHTML += '<button class="pop-up__btn pop-up__btn-fill" onclick="popupDissmiss()">Nooooooo</button>';

    // Show popup
    popup.classList.add('pop-up__active');
}

function popupDissmiss() {
    // un-Stop scrolling
    document.querySelector("html").style.overflow = "auto";

    var popup = document.querySelector('.pop-up');

    popup.classList.add('pop-up__hide');

    setTimeout(function() {
        popup.classList = 'pop-up';
    }, 200);
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        if (document.querySelector('.pop-up').classList.contains('pop-up__active')) {
            popupDissmiss();
        }
    }
});