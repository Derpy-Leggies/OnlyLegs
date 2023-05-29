function keepSquare() {
    let square = document.getElementsByClassName('square')
    for (let i = 0; i < square.length; i++) {
        square[i].style.height = square[i].offsetWidth + 'px';
    }
}