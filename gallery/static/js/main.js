let navToggle = true;

document.onscroll = function() {
    document.querySelector('.background-decoration').style.opacity = `${1 - window.scrollY / 621}`;
    document.querySelector('.background-decoration').style.top = `-${window.scrollY / 5}px`;

    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        document.querySelector('.jumpUp').style.opacity = 1;
        document.querySelector('.jumpUp').style.right = "0.75rem";
    } else {
        document.querySelector('.jumpUp').style.opacity = 0;
        document.querySelector('.jumpUp').style.right = "-3rem";
    }
}

document.querySelector('.jumpUp').onclick = function() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function imgFade(obj) {
    $(obj).animate({opacity: 1}, 500);
}

var times = document.getElementsByClassName('time');
for (var i = 0; i < times.length; i++) {
    var time = times[i].innerHTML;
    var date = new Date(time);
    times[i].innerHTML = date.toLocaleString('en-GB');
}

function addNotification(text='Sample notification', type=4) {
    var container = document.querySelector('.notifications');

    // Create notification element
    var div = document.createElement('div');
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
    var icon = document.createElement('span');
    icon.classList.add('sniffle__notification-icon');
    switch (type) {
        case 1:
            div.classList.add('sniffle__notification--success');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-5 -7 24 24" fill="currentColor">\
                <path d="M5.486 9.73a.997.997 0 0 1-.707-.292L.537 5.195A1 1 0 1 1 1.95 3.78l3.535 3.535L11.85.952a1 1 0 0 1 1.415 1.414L6.193 9.438a.997.997 0 0 1-.707.292z"></path>\
            </svg>';
            break;
        case 2:
            div.classList.add('sniffle__notification--error');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 24 24" fill="currentColor">\
                <path d="M7.314 5.9l3.535-3.536A1 1 0 1 0 9.435.95L5.899 4.485 2.364.95A1 1 0 1 0 .95 2.364l3.535 3.535L.95 9.435a1 1 0 1 0 1.414 1.414l3.535-3.535 3.536 3.535a1 1 0 1 0 1.414-1.414L7.314 5.899z"></path>\
            </svg>';
            break;
        case 3:
            div.classList.add('sniffle__notification--warning');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -3 24 24" fill="currentColor">\
                <path d="M12.8 1.613l6.701 11.161c.963 1.603.49 3.712-1.057 4.71a3.213 3.213 0 0 1-1.743.516H3.298C1.477 18 0 16.47 0 14.581c0-.639.173-1.264.498-1.807L7.2 1.613C8.162.01 10.196-.481 11.743.517c.428.276.79.651 1.057 1.096zm-2.22.839a1.077 1.077 0 0 0-1.514.365L2.365 13.98a1.17 1.17 0 0 0-.166.602c0 .63.492 1.14 1.1 1.14H16.7c.206 0 .407-.06.581-.172a1.164 1.164 0 0 0 .353-1.57L10.933 2.817a1.12 1.12 0 0 0-.352-.365zM10 14a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm0-9a1 1 0 0 1 1 1v4a1 1 0 0 1-2 0V6a1 1 0 0 1 1-1z"></path>\
            </svg>';
            break;
        default:
            div.classList.add('sniffle__notification--info');
            icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 24 24" fill="currentColor">\
                <path d="M10 20C4.477 20 0 15.523 0 10S4.477 0 10 0s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm0-10a1 1 0 0 1 1 1v5a1 1 0 0 1-2 0V9a1 1 0 0 1 1-1zm0-1a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"></path>\
            </svg>';
            break;
    }
    div.appendChild(icon);

    // Create text element and append to notification
    var description = document.createElement('span');
    description.classList.add('sniffle__notification-text');
    description.innerHTML = text;
    div.appendChild(description);

    // Create span to show time remaining
    var timer = document.createElement('span');
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

function popUpShow(title, body, actions, content) {
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
    var popup = document.querySelector('.pop-up');
    popup.classList.remove('pop-up__active');
}