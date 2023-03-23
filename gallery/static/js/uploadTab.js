window.addEventListener("dragover",(event) => {
  event.preventDefault();
},false);
window.addEventListener("drop",(event) => {
  event.preventDefault();
},false);

function fileChanged(obj) {
    document.querySelector('.fileDrop-block').classList.remove('error');

    if ($(obj).val() === '') {
        document.querySelector('.fileDrop-block').classList.remove('active');
        document.querySelector('.fileDrop-block .status').innerHTML = 'Choose or Drop file';
    } else {
        document.querySelector('.fileDrop-block').classList.add('active');
        document.querySelector('.fileDrop-block .status').innerHTML = obj.files[0].name;
    }
}

document.addEventListener('DOMContentLoaded', function() {
   // Function to upload images
    const uploadForm = document.querySelector('#uploadForm');
    const fileDrop = document.querySelector('.fileDrop-block');
    const fileDropTitle = fileDrop.querySelector('.status');
    const fileUpload = uploadForm.querySelector('#file');


    $(fileUpload).val('');


    // Choose or drop file button
    ['dragover', 'dragenter'].forEach(eventName => {
        fileDrop.addEventListener(eventName, fileActivate, false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
      fileDrop.addEventListener(eventName, fileDefault, false);
    })

    // Drop file into box
    fileDrop.addEventListener('drop', fileDropHandle, false);


    // Edging the file plunge :3
    function fileActivate(event) {
        fileDrop.classList.remove('error');
        fileDrop.classList.add('edging');
        fileDropTitle.innerHTML = 'Drop to upload!';
    }
    function fileDefault(event) {
        fileDrop.classList.remove('error');
        fileDrop.classList.remove('edging');
        fileDropTitle.innerHTML = 'Choose or Drop file';
    }

    function fileDropHandle(event) {
        event.preventDefault()
        fileUpload.files = event.dataTransfer.files;

        fileDropTitle.innerHTML = fileUpload.files[0].name;
        fileDrop.classList.add('active');
    }


    uploadForm.addEventListener('submit', (event) => {
        // AJAX takes control of subby form
        event.preventDefault()

        const jobList = document.querySelector(".upload-jobs");

        // Check for empty upload
        if ($(fileUpload).val() === '') {
            fileDrop.classList.add('error');
            fileDropTitle.innerHTML = 'No file selected!';
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
                beforeSend: function () {
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
            $(fileUpload).val('');
            $("#alt").val('');
            $("#description").val('');
            $("#tags").val('');

            // Reset drop
            fileDrop.classList.remove('active');
            fileDropTitle.innerHTML = 'Choose or Drop file';
        }
    });
});

// open upload tab
function openUploadTab() {
    // Stop scrolling
    document.querySelector("html").style.overflow = "hidden";
    document.querySelector(".content").tabIndex = "-1";

    // Open upload tab
    const uploadTab = document.querySelector(".upload-panel");
    uploadTab.style.display = "block";

    setTimeout(function () {
        uploadTab.classList.add("open");
    }, 10);
}

// close upload tab
function closeUploadTab() {
    // un-Stop scrolling
    document.querySelector("html").style.overflow = "auto";
    document.querySelector(".content").tabIndex = "";

    // Close upload tab
    const uploadTab = document.querySelector(".upload-panel");
    uploadTab.classList.remove("open");

    setTimeout(function () {
        uploadTab.style.display = "none";
    }, 250);
}

// toggle upload tab
function toggleUploadTab() {
    if (document.querySelector(".upload-panel").classList.contains("open")) {
        closeUploadTab();
    } else {
        openUploadTab();
    }
}
