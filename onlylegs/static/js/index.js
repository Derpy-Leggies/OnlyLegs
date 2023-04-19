// fade in images
function imgFade(obj, time = 250) {
    obj.style.transition = `opacity ${time}ms`;
    obj.style.opacity = 1;
}
// Lazy load images when they are in view
function loadOnView() {
    const lazyLoad = document.querySelectorAll('#lazy-load');
    const webpSupport = checkWebpSupport();

    for (let i = 0; i < lazyLoad.length; i++) {
        let image = lazyLoad[i];
        if (image.getBoundingClientRect().top < window.innerHeight && image.getBoundingClientRect().bottom > 0) {
            if (!image.src && webpSupport) {
                image.src = `${image.getAttribute('data-src')}&e=webp`;
            } else if (!image.src) {
                image.src = image.getAttribute('data-src');
            }
        }
    }
}

window.onload = function () {
    loadOnView();

    const times = document.querySelectorAll('.time');
    for (let i = 0; i < times.length; i++) {
        // Remove milliseconds
        const raw = times[i].innerHTML.split('.')[0];

        // Parse YYYY-MM-DD HH:MM:SS to Date object
        const time = raw.split(' ')[1];
        const date = raw.split(' ')[0].split('-');

        // Format to YYYY/MM/DD HH:MM:SS and convert to UTC Date object
        const dateTime = new Date(`${date[0]}/${date[1]}/${date[2]} ${time} UTC`);

        // Convert to local time
        times[i].innerHTML = `${dateTime.toLocaleDateString()} ${dateTime.toLocaleTimeString()}`;
    }

    // Top Of Page button
    const topOfPage = document.querySelector('.top-of-page');
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        topOfPage.classList.add('show');
    } else {
        topOfPage.classList.remove('show');
    }
    topOfPage.onclick = function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }

    // Info button
    const infoButton = document.querySelector('.info-button');
    if (infoButton) {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
            infoButton.classList.remove('show');
        } else {
            infoButton.classList.add('show');
        }
        infoButton.onclick = function () {
            popUpShow('OnlyLegs',
                      '<a href="https://github.com/Fluffy-Bean/onlylegs">v0.1.0</a> ' +
                      'using <a href="https://phosphoricons.com/">Phosphoricons</a> and Flask.' +
                      '<br>Made by Fluffy and others with ❤️');
        }
    }
};
window.onscroll = function () {
    loadOnView();

    // Top Of Page button
    const topOfPage = document.querySelector('.top-of-page');
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        topOfPage.classList.add('show');
    } else {
        topOfPage.classList.remove('show');
    }

    // Info button
    const infoButton = document.querySelector('.info-button');
    if (infoButton) {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
            infoButton.classList.remove('show');
        } else {
            infoButton.classList.add('show');
        }
    }
};
window.onresize = function () {
    loadOnView();
};
