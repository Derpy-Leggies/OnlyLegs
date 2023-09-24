function popupShow(titleText, subtitleText, bodyContent=null, userActions=null) {
    // Get popup elements
    const popupSelector = document.querySelector('.pop-up');
    const headerSelector = document.querySelector('.pop-up-header');
    const actionsSelector = document.querySelector('.pop-up-controlls');

    // Clear popup elements
    headerSelector.innerHTML = '';
    actionsSelector.innerHTML = '';

    // Set popup header and subtitle
    if (titleText) {
        let titleElement = document.createElement('h2');
            titleElement.innerHTML = titleText;
            headerSelector.appendChild(titleElement);
    }

    if (subtitleText) {
        let subtitleElement = document.createElement('p');
            subtitleElement.innerHTML = subtitleText;
            headerSelector.appendChild(subtitleElement);
    }

    if (bodyContent) { headerSelector.appendChild(bodyContent) }

    // Set buttons that will be displayed
    if (userActions) {
        userActions.forEach((action) => {
            actionsSelector.appendChild(action);
        });
    } else {
        let closeButton = document.createElement('button');
            closeButton.classList.add('btn-block');
            closeButton.classList.add('transparent');
            closeButton.innerHTML = 'Yeet!';
            closeButton.onclick = popupDismiss;
        actionsSelector.appendChild(closeButton);
    }

    // Stop scrolling and show popup
    document.querySelector("html").style.overflow = "hidden";
    popupSelector.style.display = 'block';

    // 5ms delay to allow for css transition >:C
    setTimeout(() => { popupSelector.classList.add('active') }, 5);
}

function popupDismiss() {
    const popupSelector = document.querySelector('.pop-up');
    document.querySelector("html").style.overflow = "auto";
    popupSelector.classList.remove('active');
    setTimeout(() => { popupSelector.style.display = 'none'; }, 200);
}

const popupCancelButton = document.createElement('button');
      popupCancelButton.classList.add('btn-block');
      popupCancelButton.classList.add('transparent');
      popupCancelButton.innerHTML = 'nuuuuuuuu';
      popupCancelButton.onclick = popupDismiss;
