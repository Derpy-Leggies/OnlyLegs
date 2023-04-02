// fade in images
function imgFade(obj, time = 250) {
    $(obj).animate({ opacity: 1 }, time);
}
// Lazy load images when they are in view
function loadOnView() {
    let lazyLoad = document.querySelectorAll('#lazy-load');

    for (let i = 0; i < lazyLoad.length; i++) {
        let image = lazyLoad[i];
        if (image.getBoundingClientRect().top < window.innerHeight && image.getBoundingClientRect().bottom > 0) {
            if (!image.src) {
                image.src = `/api/file/${image.getAttribute('data-src')}?r=thumb` // e=webp
            }
        }
    }
}

window.onload = function () {
    loadOnView();

    let times = document.querySelectorAll('.time');
    for (let i = 0; i < times.length; i++) {
        // Remove milliseconds
        const raw = times[i].innerHTML.split('.')[0];

        // Parse YYYY-MM-DD HH:MM:SS to Date object
        const time = raw.split(' ')[1]
        const date = raw.split(' ')[0].split('-');

        // Format to YYYY/MM/DD HH:MM:SS
        let formatted = date[0] + '/' + date[1] + '/' + date[2] + ' ' + time + ' UTC';

        // Convert to UTC Date object
        let dateTime = new Date(formatted);

        // Convert to local time
        times[i].innerHTML = dateTime.toLocaleDateString() + ' ' + dateTime.toLocaleTimeString();
    }

    // Top Of Page button
    let topOfPage = document.querySelector('.top-of-page');
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
    let infoButton = document.querySelector('.info-button');

    if (infoButton) {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
            infoButton.classList.remove('show');
        } else {
            infoButton.classList.add('show');
        }
        infoButton.onclick = function () {
            popUpShow('OnlyLegs on Flask',
                      'Using <a href="https://phosphoricons.com/">Phosphoricons</a> and ' +
                      '<a href="https://www.gent.media/manrope">Manrope</a> <br>' +
                      'Made by Fluffy and others with ❤️ <br>' +
                      '<a href="https://github.com/Fluffy-Bean/onlylegs">V23.04.02</a>');
        }
    }
};
window.onscroll = function () {
    loadOnView();

    // Top Of Page button
    let topOfPage = document.querySelector('.top-of-page');
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        topOfPage.classList.add('show');
    } else {
        topOfPage.classList.remove('show');
    }

    // Info button
    let infoButton = document.querySelector('.info-button');

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
