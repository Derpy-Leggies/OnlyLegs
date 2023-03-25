// fade in images
function imgFade(obj, time = 250) {
    $(obj).animate({ opacity: 1 }, time);
}
// https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
function colourContrast(bgColor, lightColor, darkColor, threshold = 0.179) {
    // if color is in hex format then convert to rgb else parese rgb
    let r = 0
    let g = 0
    let b = 0
    if (bgColor.charAt(0) === '#') {
        const color = (bgColor.charAt(0) === '#') ? bgColor.substring(1, 7) : bgColor;
        r = parseInt(color.substring(0, 2), 16); // hexToR
        g = parseInt(color.substring(2, 4), 16); // hexToG
        b = parseInt(color.substring(4, 6), 16); // hexToB
    } else {
        const color = bgColor.replace('rgb(', '').replace(')', '').split(',');
        r = color[0];
        g = color[1];
        b = color[2];
    }
    
    const uicolors = [r / 255, g / 255, b / 255];
    const c = uicolors.map((col) => {
        if (col <= 0.03928) {
            return col / 12.92;
        }
        return Math.pow((col + 0.055) / 1.055, 2.4);
    });
    const L = (0.2126 * c[0]) + (0.7152 * c[1]) + (0.0722 * c[2]);
    return (L > threshold) ? darkColor : lightColor;
}
// Lazy load images when they are in view
function loadOnView() {
    let lazyLoad = document.querySelectorAll('#lazy-load');

    for (let i = 0; i < lazyLoad.length; i++) {
        let image = lazyLoad[i];
        if (image.getBoundingClientRect().top < window.innerHeight && image.getBoundingClientRect().bottom > 0) {
            if (!image.src) {
                image.src = `/api/file/${image.getAttribute('data-src')}?r=thumb`
            }
        }
    }
}

window.onload = function () {
    loadOnView();

    const darkColor = '#151515';
    const lightColor = '#E8E3E3';
    let contrastCheck = document.querySelectorAll('#contrast-check');
    for (let i = 0; i < contrastCheck.length; i++) {
        let bgColor = contrastCheck[i].getAttribute('data-color');
        contrastCheck[i].style.color = colourContrast(bgColor, lightColor, darkColor);
    }

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
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        infoButton.classList.remove('show');
    } else {
        infoButton.classList.add('show');
    }
    infoButton.onclick = function () {
        popUpShow('OnlyLegs Gallery',
                  'Using <a href="https://phosphoricons.com/">Phosphoricons</a> and <a href="https://www.gent.media/manrope">Manrope</a> <br>' +
                  'Made by Fluffy and others with ❤️ <br>' +
                  '<a href="https://github.com/Fluffy-Bean/onlylegs">V23.03.25</a>');
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
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        infoButton.classList.remove('show');
    } else {
        infoButton.classList.add('show');
    }
};
window.onresize = function () {
    loadOnView();
};
