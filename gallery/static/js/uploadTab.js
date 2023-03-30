// Remove default events on file drop, otherwise the browser will open the file
window.addEventListener("dragover", (event) => {
    event.preventDefault();
}, false);
window.addEventListener("drop", (event) => {
    event.preventDefault();
}, false);


// open upload tab
function openUploadTab() {
    let uploadTab = document.querySelector(".upload-panel");

    // Stop scrolling and open upload tab
    document.querySelector("html").style.overflow = "hidden";
    uploadTab.style.display = "block";
    setTimeout(function () { uploadTab.classList.add("open"); }, 5);
}

// close upload tab
function closeUploadTab() {
    let uploadTab = document.querySelector(".upload-panel");

    // un-Stop scrolling and close upload tab
    document.querySelector("html").style.overflow = "auto";
    uploadTab.classList.remove("open");
    setTimeout(function () { uploadTab.style.display = "none"; }, 250);
}

// toggle upload tab
function toggleUploadTab() {
    let uploadTab = document.querySelector(".upload-panel");

    if (uploadTab.classList.contains("open")) {
        closeUploadTab();
    } else {
        openUploadTab();
    }
}

// Edging the file plunge :3
function fileActivate(event) {
    event.preventDefault()

    let fileDrop = document.querySelector('.fileDrop-block');
    let fileDropTitle = fileDrop.querySelector('.status');

    fileDrop.classList.remove('error');
    fileDrop.classList.add('edging');
    fileDropTitle.innerHTML = 'Drop to upload!';
}
function fileDefault() {
    let fileDrop = document.querySelector('.fileDrop-block');
    let fileDropTitle = fileDrop.querySelector('.status');

    fileDrop.classList.remove('error');
    fileDrop.classList.remove('edging');
    fileDropTitle.innerHTML = 'Choose or Drop file';
}

function fileDropHandle(event) {
    event.preventDefault()

    let fileDrop = document.querySelector('.fileDrop-block');
    let fileUpload = fileDrop.querySelector('#file');

    fileUpload.files = event.dataTransfer.files;
    
    fileChanged();
}

function fileChanged() {
    let dropBlock = document.querySelector('.fileDrop-block');
    let dropBlockStatus = dropBlock.querySelector('.status');
    let dropBlockInput = dropBlock.querySelector('#file');

    if (dropBlockInput.value !== "") {
        dropBlock.classList.add('active');
        dropBlockStatus.innerHTML = dropBlockInput.files[0].name;
    } else {
        fileDefault();
    }
}

function clearUpload() {
    let fileDrop = document.querySelector('#uploadForm');

    let fileUpload = fileDrop.querySelector('#file');
    let fileAlt = fileDrop.querySelector('#alt');
    let fileDescription = fileDrop.querySelector('#description');
    let fileTags = fileDrop.querySelector('#tags');

    fileUpload.value = "";
    fileAlt.value = "";
    fileDescription.value = "";
    fileTags.value = "";
}


function createJon(file) {
    jobContainer = document.createElement("div");
    jobContainer.classList.add("job");

    jobStatus = document.createElement("span");
    jobStatus.classList.add("job__status");
    jobStatus.innerHTML = "Uploading...";

    jobProgress = document.createElement("span");
    jobProgress.classList.add("progress");

    jobImg = document.createElement("img");
    jobImg.src = URL.createObjectURL(file);

    jobImgFilter = document.createElement("span");
    jobImgFilter.classList.add("img-filter");

    jobContainer.appendChild(jobStatus);
    jobContainer.appendChild(jobProgress);
    jobContainer.appendChild(jobImg);
    jobContainer.appendChild(jobImgFilter);
    
    return jobContainer;
}


document.addEventListener('DOMContentLoaded', function() {
   // Function to upload images
    let uploadForm = document.querySelector('#uploadForm');
    let fileDrop = document.querySelector('.fileDrop-block');
    let fileDropTitle = fileDrop.querySelector('.status');
    let jobList = document.querySelector(".upload-jobs");
    
    let fileUpload = uploadForm.querySelector('#file');
    let fileAlt = uploadForm.querySelector('#alt');
    let fileDescription = uploadForm.querySelector('#description');
    let fileTags = uploadForm.querySelector('#tags');


    clearUpload();
    fileDefault();


    // Drag over/enter event
    fileDrop.addEventListener('dragover', fileActivate, false);
    fileDrop.addEventListener('dragenter', fileActivate, false);
    // Drag out
    fileDrop.addEventListener('dragleave', fileDefault, false);
    // Drop file into box
    fileDrop.addEventListener('drop', fileDropHandle, false);
    // File upload change
    fileUpload.addEventListener('change', fileChanged, false);


    // Submit form
    uploadForm.addEventListener('submit', (event) => {
        // AJAX takes control of subby form
        event.preventDefault()

        if (fileUpload.value === "") {
            fileDrop.classList.add('error');
            fileDropTitle.innerHTML = 'No file selected!';
            // Stop the function
            return;
        }

        // Make form
        let formData = new FormData();

        formData.append("file", fileUpload.files[0]);
        formData.append("alt", fileAlt.value);
        formData.append("description", fileDescription.value);
        formData.append("tags", fileTags.value);

        jobItem = createJon(fileUpload.files[0]);
        jobStatus = jobItem.querySelector(".job__status");

        // Upload the information
        $.ajax({
            url: '/api/upload',
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            beforeSend: function () {
                // Add job to list
                jobList.appendChild(jobItem);
            },
            success: function (response) {
                jobItem.classList.add("success");
                jobStatus.innerHTML = "Uploaded successfully";
                if (!document.querySelector(".upload-panel").classList.contains("open")) {
                    addNotification("Image uploaded successfully", 1);
                }
            },
            error: function (response) {
                jobItem.classList.add("critical");
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

        clearUpload();
        
        // Reset drop
        fileDrop.classList.remove('active');
        fileDropTitle.innerHTML = 'Choose or Drop file';
    });
});
