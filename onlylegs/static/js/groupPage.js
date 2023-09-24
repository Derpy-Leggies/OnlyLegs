function groupDeletePopup() {
    let title = 'Yeet!';
    let subtitle =
        'Are you surrrre? This action is irreversible ' +
        'and very final. This wont delete the images, ' +
        'but it will remove them from this group.'
    let body = null;

    let deleteBtn = document.createElement('button');
        deleteBtn.classList.add('btn-block');
        deleteBtn.classList.add('critical');
        deleteBtn.innerHTML = 'Dewww eeeet!';
        deleteBtn.onclick = groupDeleteConfirm;

    popupShow(title, subtitle, body, [popupCancelButton, deleteBtn]);
}

function groupDeleteConfirm(event) {
    // AJAX takes control of subby form :3
    event.preventDefault();

    fetch('/group/' + group_data['id'], {
        method: 'DELETE',
    }).then(response => {
        if (response.ok) {
            window.location.href = '/group/';
        } else {
            addNotification('Server exploded, returned:' + response.status, 2);
        }
    }).catch(error => {
        addNotification('Error yeeting group!' + error, 2);
    });
}

function groupEditPopup() {
    let title = 'Nothing stays the same';
    let subtitle = 'Add, remove, or change, the power is in your hands...'

    let formSubmitButton = document.createElement('button');
        formSubmitButton.setAttribute('form', 'groupEditForm');
        formSubmitButton.setAttribute('type', 'submit');
        formSubmitButton.classList.add('btn-block');
        formSubmitButton.classList.add('primary');
        formSubmitButton.innerHTML = 'Saveeee';

    // Create form
    let body = document.createElement('form');
        body.setAttribute('onsubmit', 'return groupEditConfirm(event);');
        body.id = 'groupEditForm';

    let formImageId = document.createElement('input');
        formImageId.setAttribute('type', 'text');
        formImageId.setAttribute('placeholder', 'Image ID');
        formImageId.setAttribute('required', '');
        formImageId.classList.add('input-block');
        formImageId.id = 'groupFormImageId';

    let formAction = document.createElement('input');
        formAction.setAttribute('type', 'text');
        formAction.setAttribute('value', 'add');
        formAction.setAttribute('placeholder', '[add, remove]');
        formAction.setAttribute('required', '');
        formAction.classList.add('input-block');
        formAction.id = 'groupFormAction';

    body.appendChild(formImageId);
    body.appendChild(formAction);

    popupShow(title, subtitle, body, [popupCancelButton, formSubmitButton]);
}

function groupEditConfirm(event) {
    // AJAX takes control of subby form :3
    event.preventDefault();

    let imageId = document.querySelector("#groupFormImageId").value;
    let action = document.querySelector("#groupFormAction").value;
    let formData = new FormData();
        formData.append("imageId", imageId);
        formData.append("action", action);

    fetch('/group/' + group_data['id'], {
        method: 'PUT',
        body: formData
    }).then(response => {
       if (response.ok) {
            window.location.reload();
        } else {
            addNotification('Server exploded, returned:' + response.status, 2);
        }
    }).catch(error => {
        addNotification('Error!!!!! Panic!!!!' + error, 2);
    });
}

function groupCreatePopup() {
    let title = 'New stuff!';
    let subtitle =
        'Image groups are a simple way to ' +
        '"group" images together, are you ready?'

    let formSubmitButton = document.createElement('button');
        formSubmitButton.setAttribute('form', 'groupCreateForm');
        formSubmitButton.setAttribute('type', 'submit');
        formSubmitButton.classList.add('btn-block');
        formSubmitButton.classList.add('primary');
        formSubmitButton.innerHTML = 'Huzzah!';

    // Create form
    let body = document.createElement('form');
        body.setAttribute('onsubmit', 'return groupCreateConfirm(event);');
        body.id = 'groupCreateForm';

    let formName = document.createElement('input');
        formName.setAttribute('type', 'text');
        formName.setAttribute('placeholder', 'Group namey');
        formName.setAttribute('required', '');
        formName.classList.add('input-block');
        formName.id = 'groupFormName';

    let formDescription = document.createElement('input');
        formDescription.setAttribute('type', 'text');
        formDescription.setAttribute('placeholder', 'What it about????');
        formDescription.classList.add('input-block');
        formDescription.id = 'groupFormDescription';

    body.appendChild(formName);
    body.appendChild(formDescription);

    popupShow(title, subtitle, body, [popupCancelButton, formSubmitButton]);
}

function groupCreateConfirm(event) {
    // AJAX takes control of subby form :3
    event.preventDefault();

    let name = document.querySelector("#groupFormName").value;
    let description = document.querySelector("#groupFormDescription").value;
    let formData = new FormData();
        formData.append("name", name);
        formData.append("description", description);

    fetch('/group/', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            addNotification('Server exploded, returned:' + response.status, 2);
        }
    }).catch(error => {
        addNotification('Error summoning group!' + error, 2);
    });
}