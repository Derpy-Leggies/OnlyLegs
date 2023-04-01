document.addEventListener('DOMContentLoaded', function() {
    let labels = document.querySelectorAll('[data-label]');

    for (let i = 0; i < labels.length; i++) {
        labels[i].addEventListener('mouseover', function() {
            let label = document.createElement('div');
            label.classList.add('label');
            label.innerHTML = this.dataset.label;

            document.body.appendChild(label);

            label.style.left = (this.offsetLeft + this.offsetWidth + 8) + 'px';
            label.style.top = (this.offsetTop + (label.offsetHeight / 2) - 2) + 'px';

            setTimeout(function() {
                label.style.opacity = 1;
            }.bind(this), 250);
        });

        labels[i].addEventListener('mouseout', function() {
            let label = document.querySelector('.label');
            label.parentNode.removeChild(label);
        });
    }
});
