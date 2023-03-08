function uploadFile(){
    // AJAX takes control of subby form
    event.preventDefault();

    const jobList = document.querySelector(".upload-jobs");

    // Check for empty upload
    if ($("#file").val() === "") {
        addNotification("Please select a file to upload", 2);
    } else {
        // Make form
        let formData = new FormData();
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
            beforeSend: function() {
                jobContainer = document.createElement("div");
                jobContainer.classList.add("job");

                jobStatus = document.createElement("span");
                jobStatus.classList.add("job__status");
                jobStatus.innerHTML = "Uploading...";
                
                jobProgress = document.createElement("span");
                jobProgress.classList.add("progress");

                jobImg = document.createElement("img");
                jobImg.src = URL.createObjectURL($("#file").prop("files")[0]);

                jobImgFilter = document.createElement("span");
                jobImgFilter.classList.add("img-filter");

                jobContainer.appendChild(jobStatus);
                jobContainer.appendChild(jobProgress);
                jobContainer.appendChild(jobImg);
                jobContainer.appendChild(jobImgFilter);
                jobList.appendChild(jobContainer);
            },
            success: function (response) {
                jobContainer.classList.add("success");
                jobStatus.innerHTML = "Uploaded!";
                if (!document.querySelector(".upload-panel").classList.contains("open")) {
                    addNotification("Image uploaded successfully", 1);
                }
            },
            error: function (response) {
                jobContainer.classList.add("critical");
                switch (response.status) {
                    case 500:
                        jobStatus.innerHTML = "Server exploded, F's in chat";
                        break;
                    case 400:
                    case 404:
                        jobStatus.innerHTML = "Error uploading. Blame yourself";
                        break;
                    case 403:
                        jobStatus.innerHTML = "None but devils play past here...";
                        break;
                    case 413:
                        jobStatus.innerHTML = "File too large!!!!!!";
                        break;
                    default:
                        jobStatus.innerHTML = "Error uploading file, blame someone";
                        break;
                }
                if (!document.querySelector(".upload-panel").classList.contains("open")) {
                    addNotification("Error uploading file", 2);
                }
            },
        });

        // Empty values
        $("#file").val("");
        $("#alt").val("");
        $("#description").val("");
        $("#tags").val("");
    }
};

function openUploadTab() {
    // Open upload tab
    const uploadTab = document.querySelector(".upload-panel");
    uploadTab.style.display = "block";

    setTimeout( function() {
        uploadTab.classList.add("open");
    }, 10);
}

function closeUploadTab() {
    // Close upload tab
    const uploadTab = document.querySelector(".upload-panel");
    uploadTab.classList.remove("open");
    setTimeout( function() {
        uploadTab.style.display = "none";
    }, 250);
}