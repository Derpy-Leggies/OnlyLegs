// fade in images
function imgFade(obj, time = 200) {
    setTimeout(() => {
        obj.style.animation = `imgFadeIn ${time}ms`;

        setTimeout(() => {
            obj.style.opacity = null;
            obj.style.animation = null;
        }, time);
    }, 1);
}
