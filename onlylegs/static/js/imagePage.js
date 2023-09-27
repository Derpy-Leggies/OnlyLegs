function imageFullscreen() {
    let info = document.querySelector('.info-container');
    let image = document.querySelector('.image-container');

    if (info.classList.contains('collapsed')) {
        info.classList.remove('collapsed');
        image.classList.remove('collapsed');
        document.cookie = "image-info=0"
    } else {
        info.classList.add('collapsed');
        image.classList.add('collapsed');
        document.cookie = "image-info=1"
    }
}

function imageShowOptionsPopup(obj) {
    showContextMenu(obj, [
        {
            'value': 'Edit',
            'function': () => {
                dissmissContextMenu();
                imageEditPopup();
            },
            'type': 'critical',
            'icon': '<i class="ph-fill ph-pencil"></i>'
        },
        {
            'value': 'Delete',
            'function': () => {
                dissmissContextMenu();
                imageDeletePopup();
            },
            'type': 'critical',
            'icon': '<i class="ph-fill ph-trash"></i>'
        }
    ], 'button')
}

function imageDeletePopup() {
    let title = 'DESTRUCTION!!!!!!';
    let subtitle =
        'Do you want to delete this image along with ' +
        'all of its data??? This action is irreversible!';
    let body = null;

    let deleteBtn = document.createElement('button');
        deleteBtn.classList.add('btn-block');
        deleteBtn.classList.add('critical');
        deleteBtn.innerHTML = 'Dewww eeeet!';
        deleteBtn.onclick = imageDeleteConfirm;

    popupShow(title, subtitle, body, [popupCancelButton, deleteBtn]);
}
function imageDeleteConfirm() {
    popupDismiss();

    fetch('/image/' + image_data["id"], {
        method: 'DELETE',
    }).then(response => {
        if (response.ok) {
            window.location.href = '/';
        } else {
            addNotification('Image *clings*', 2);
        }
    });
}

function imageEditPopup() {
    let title = 'Edit image!';
    let subtitle = 'Enter funny stuff here!';

    let formSubmitButton = document.createElement('button');
        formSubmitButton.setAttribute('form', 'imageEditForm');
        formSubmitButton.setAttribute('type', 'submit');
        formSubmitButton.classList.add('btn-block');
        formSubmitButton.classList.add('primary');
        formSubmitButton.innerHTML = 'Saveeee';

    // Create form
    let body = document.createElement('form');
        body.setAttribute('onsubmit', 'return imageEditConfirm(event);');
        body.id = 'imageEditForm';

    let formAlt = document.createElement('input');
        formAlt.setAttribute('type', 'text');
        formAlt.setAttribute('value', image_data["alt"]);
        formAlt.setAttribute('placeholder', 'Image Alt');
        formAlt.classList.add('input-block');
        formAlt.id = 'imageFormAlt';

    let formDescription = document.createElement('input');
        formDescription.setAttribute('type', 'text');
        formDescription.setAttribute('value', image_data["description"]);
        formDescription.setAttribute('placeholder', 'Image Description');
        formDescription.classList.add('input-block');
        formDescription.id = 'imageFormDescription';

    body.appendChild(formAlt);
    body.appendChild(formDescription);

    popupShow(title, subtitle, body, [popupCancelButton, formSubmitButton]);
}

function imageEditConfirm(event) {
    // Yoink subby form
    event.preventDefault();

    let alt = document.querySelector('#imageFormAlt').value;
    let description = document.querySelector('#imageFormDescription').value;
    let form = new FormData();
        form.append('alt', alt);
        form.append('description', description);

    fetch('/image/' + image_data["id"], {
        method: 'PUT',
        body: form,
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            addNotification('Image *clings*', 2);
        }
    });
}
