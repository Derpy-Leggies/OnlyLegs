function showUpload() {
    popUpShow(
        'Upload funny stuff',
        'May the world see your stuff 👀',
        '',
        '<form onsubmit="return uploadFile(event)">\
            <input class="pop-up__input" type="file" id="file"/>\
            <input class="pop-up__input" type="text" placeholder="alt" id="alt"/>\
            <input class="pop-up__input" type="text" placeholder="description" id="description"/>\
            <input class="pop-up__input" type="text" placeholder="tags" id="tags"/>\
            <button class="pop-up__btn pop-up__btn-primary-fill">Upload</button>\
        </form>'
    );
};
function uploadFile(){
    // AJAX takes control of subby form
    event.preventDefault();

    // Check for empty upload
    if ($("#file").val() === "") {
        addNotification("Please select a file to upload", 2);
    } else {
        // Make form
        var formData = new FormData();
        formData.append("file", $("#file").prop("files")[0]);
        formData.append("alt", $("#alt").val());
        formData.append("description", $("#description").val());
        formData.append("tags", $("#tags").val());
        formData.append("submit", $("#submit").val());

        // Upload the information
        $.ajax({
            url: '/api/upload',
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                addNotification("File uploaded successfully!", 1);
                // popupDissmiss(); // Close popup
            },
            error: function (response) {
                switch (response.status) {
                    case 500:
                        addNotification('Server exploded, F\'s in chat', 2);
                        break;
                    case 400:
                    case 404:
                        addNotification('Error uploading. Blame yourself', 2);
                        break;
                    case 403:
                        addNotification('None but devils play past here...', 2);
                        break;
                    case 413:
                        addNotification('File too large!!!!!!', 3);
                        break;
                    default:
                        addNotification('Error uploading file, blame someone', 2);
                        break;
                }
            }
        });

        // Empty values
        $("#file").val("");
        $("#alt").val("");
        $("#description").val("");
        $("#tags").val("");
    }
};