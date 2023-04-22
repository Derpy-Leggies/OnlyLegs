function keepSquare() {
    const images = document.querySelectorAll('.gallery-item');
    for (let i = 0; i < images.length; i++) {
        images[i].style.height = images[i].offsetWidth + 'px';
    }

    const groups = document.querySelectorAll('.group-item');
    for (let i = 0; i < groups.length; i++) {
        groups[i].style.height = groups[i].offsetWidth + 'px';
    }
}