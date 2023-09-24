function showContextMenu(obj, menu, position='mouse') {
    // If the context menu is already open, close it first
    if (document.querySelector(".contextMenu")) {
        dissmissContextMenu();
    }

    // Add span to close the context menu
    let contextCloseSpan = document.createElement("span");
        contextCloseSpan.className = "contextMenuClose";
        contextCloseSpan.onclick = dissmissContextMenu;

    // Create the context menu
    let contextMenu = document.createElement("div");
        contextMenu.className = "contextMenu";

    // Create the menu items
    menu.forEach(array => {
        if (array.value === "divider") {
            let divider = document.createElement("hr");
                divider.className = "contextMenuDivider";

            contextMenu.appendChild(divider);
            return;
        } else if (array['value'] === "title") {
            let titleP = document.createElement("p");
                titleP.className = "contextMenuTitle";
                titleP.innerHTML = array.text;

            contextMenu.appendChild(titleP);
            let divider = document.createElement("hr");
                divider.className = "contextMenuDivider";

            contextMenu.appendChild(divider);
            return;
        }

        let itemBtn = document.createElement("button");
            itemBtn.className = "contextMenuItem";
            itemBtn.onclick = array['function'];

        if (array['type'] === "critical") {
            itemBtn.classList.add("contextMenuItem__critical");
        } else if (array['type'] === "warning") {
            itemBtn.classList.add("contextMenuItem__warning");
        } else if (array['type'] === "success") {
            itemBtn.classList.add("contextMenuItem__success");
        } else if (array['type'] === "info") {
            itemBtn.classList.add("contextMenuItem__info");
        }

        let itemIcon = document.createElement("span");
            itemIcon.className = "contextMenuIcon";
        if (array['icon']) {
            itemIcon.innerHTML = array['icon'];
        } else {
           itemIcon.innerHTML = '';
        }
        itemBtn.appendChild(itemIcon);

        // Create the text for the action
        let itemText = document.createElement("p");
            itemText.className = "contextMenuText";
            itemText.innerHTML = array.value;
        itemBtn.appendChild(itemText);

        contextMenu.appendChild(itemBtn);
    });

    // Add the context menu to the body
    document.body.appendChild(contextMenu);
    document.body.appendChild(contextCloseSpan);

    let posX;
    let posY;

    if (position === 'mouse') {
        posX = event.clientX + 5;
        posY = event.clientY + 5;
    } else if (position === 'button') {
        posX = obj.offsetLeft + (obj.offsetWidth / 2) - (contextMenu.offsetWidth / 2);
        posY = obj.offsetTop + obj.offsetHeight + 5;
    } else if (position === 'center') {
        posX = (window.innerWidth / 2) - (contextMenu.offsetWidth / 2);
        posY = (window.innerHeight / 2) - (contextMenu.offsetHeight / 2);
    } else {
        posX = event.clientX + 5;
        posY = event.clientY + 5;
    }

    // Move the context menu if it is off the screen
    if (posX + contextMenu.offsetWidth > window.innerWidth) {
        posX = window.innerWidth - (contextMenu.offsetWidth + 5);
    } else if (posX < 0) {
        posX = 5;
    }
    if (posY < 0) {
        posY = 5;
    }
    contextMenu.style.left = posX + "px";
    contextMenu.style.top = posY + "px";

    // Timeout otherwise animation doesn't work
    setTimeout(function() {
        if (position === 'mouse') {
            contextMenu.classList.add("contextMenu__show--mouse");
        } else if (position === 'button') {
            contextMenu.classList.add("contextMenu__show--button");
        } else if (position === 'center') {
            contextMenu.classList.add("contextMenu__show--center");
        } else {
            contextMenu.classList.add("contextMenu__show");
        }
    }, 1);
}

function dissmissContextMenu() {
    // Remove the close span
    let contextSpan = document.querySelectorAll(".contextMenuClose");
    contextSpan.forEach(menu => {
        menu.remove();
    });

    // Get the context menu
    let contextMenu = document.querySelectorAll(".contextMenu");
    contextMenu.forEach(menu => {
        menu.classList.add("contextMenu__hide");
        setTimeout(function() {
            menu.remove();
        }, 500);
    });
}

window.onresize = () => {
    dissmissContextMenu();
}
