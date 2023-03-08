let navToggle = true;

document.onscroll = function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        document.querySelector('.jumpUp').classList = 'jumpUp jumpUp--show';
    } else {
        document.querySelector('.jumpUp').classList = 'jumpUp';
    }
}

document.querySelector('.jumpUp').onclick = function() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function imgFade(obj) {
    $(obj).animate({opacity: 1}, 250);
}

let times = document.getElementsByClassName('time');
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
