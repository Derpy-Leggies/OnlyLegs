function checkWebpSupport() {
    var webpSupport = false;
    try {
        webpSupport = document.createElement('canvas').toDataURL('image/webp').indexOf('data:image/webp') === 0;
    } catch (e) {
        webpSupport = false;
    }

    return webpSupport;
}
