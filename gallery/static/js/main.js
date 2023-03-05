let navToggle = true;

document.onscroll = function() {
    try {
        document.querySelector('.background-decoration').style.opacity = `${1 - window.scrollY / 621}`;
        document.querySelector('.background-decoration').style.top = `-${window.scrollY / 5}px`;
    } catch (e) {
        // Do nothing if banner not found
    }

    try {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
            document.querySelector('.banner').classList = 'banner banner-scrolled';
        } else {
            document.querySelector('.banner').classList = 'banner';
        }
    }
    catch (e) {
        // Do nothing if banner not found
    }

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

var times = document.getElementsByClassName('time');
for (var i = 0; i < times.length; i++) {
    var time = times[i].innerHTML;
    var date = new Date(time);
    times[i].innerHTML = date.toLocaleString('en-GB');
}
