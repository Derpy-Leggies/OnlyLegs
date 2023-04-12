function popUpShow(titleText, subtitleText, bodyContent=null, userActions=null) {
    // Get popup elements
    const popupSelector = document.querySelector('.pop-up');
    const headerSelector = document.querySelector('.pop-up-header');
    const actionsSelector = document.querySelector('.pop-up-controlls');

    // Clear popup elements
    headerSelector.innerHTML = '';
    actionsSelector.innerHTML = '';

    // Set popup header and subtitle
    const titleElement = document.createElement('h2');
    titleElement.innerHTML = titleText;
    headerSelector.appendChild(titleElement);

    const subtitleElement = document.createElement('p');
    subtitleElement.innerHTML = subtitleText;
    headerSelector.appendChild(subtitleElement);

    if (bodyContent) {
        headerSelector.appendChild(bodyContent);
    }

    // Set buttons that will be displayed
    if (userActions) {
        // for each user action, add the element
        for (let i = 0; i < userActions.length; i++) {
            actionsSelector.appendChild(userActions[i]);
        }
    } else {
        actionsSelector.innerHTML = '<button class="btn-block" onclick="popupDissmiss()">Close</button>';
    }

    // Stop scrolling and show popup
    document.querySelector("html").style.overflow = "hidden";
    popupSelector.style.display = 'block';
    setTimeout(function() { popupSelector.classList.add('active') }, 5);  // 2ms delay to allow for css transition >:C
}

function popupDissmiss() {
    const popupSelector = document.querySelector('.pop-up');

    document.querySelector("html").style.overflow = "auto";
    popupSelector.classList.remove('active');
    setTimeout(function() { popupSelector.style.display = 'none'; }, 200);
}
