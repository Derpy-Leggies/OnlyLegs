function copyToClipboard(data) {
    try {
        navigator.clipboard.writeText(data)
        addNotification("Copied to clipboard!", 4);
    } catch (err) {
        addNotification("Oh noes, something when wrong D:", 2);
    }
}