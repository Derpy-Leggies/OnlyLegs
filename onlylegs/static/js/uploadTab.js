// Remove default events on file drop, otherwise the browser will open the file
window.addEventListener("dragover", (event) => {
    event.preventDefault();
}, false);
window.addEventListener("drop", (event) => {
    event.preventDefault();
}, false);


// open upload tab
function openUploadTab() {
    const uploadTab = document.querySelector(".upload-panel");

    // Stop scrolling and open upload tab
    document.querySelector("html").style.overflow = "hidden";
    uploadTab.style.display = "block";
    setTimeout(function () { uploadTab.classList.add("open"); }, 5);
}

// close upload tab
function closeUploadTab() {
    const uploadTab = document.querySelector(".upload-panel");
    const uploadTabContainer = document.querySelector(".upload-panel .container");

    // un-Stop scrolling and close upload tab
    document.querySelector("html").style.overflow = "auto";
    uploadTab.classList.remove("open");
    setTimeout(function () {
        uploadTab.style.display = "none";

        uploadTabContainer.style.transform = "";
        uploadTab.dataset.lastY = 0;
    }, 250);
}

// toggle upload tab
function toggleUploadTab() {
    const uploadTab = document.querySelector(".upload-panel");

    if (uploadTab.classList.contains("open")) {
        closeUploadTab();
    } else {
        openUploadTab();
    }
}

function tabDragStart(event) {
    event.preventDefault();

    const uploadTab = document.querySelector(".upload-panel .container");
    const offset = uploadTab.getBoundingClientRect().y;

    uploadTab.classList.add("dragging");

    document.addEventListener('touchmove', event => {
        if (uploadTab.classList.contains("dragging")) {
            if (event.touches[0].clientY - offset >= 0) {
                uploadTab.dataset.lastY = event.touches[0].clientY;
            } else {
                uploadTab.dataset.lastY = offset;
            }

            uploadTab.style.transform = `translateY(${uploadTab.dataset.lastY - offset}px)`;
        }
    });
}
function tabDragStopped(event) {
    event.preventDefault();
    
    const uploadTab = document.querySelector(".upload-panel .container");

    uploadTab.classList.remove("dragging");

    if (uploadTab.dataset.lastY > (screen.height * 0.3)) {
        closeUploadTab();
    } else {
        uploadTab.style.transition = "transform 0.25s cubic-bezier(0.76, 0, 0.17, 1)";
        uploadTab.style.transform = "translateY(0px)";
        setTimeout(function () { uploadTab.style.transition = ""; }, 250);
    }
}


// Edging the file plunge :3
function fileActivate(event) {
    event.preventDefault()

    const fileDrop = document.querySelector('.fileDrop-block');
    const fileDropTitle = fileDrop.querySelector('.status');

    fileDrop.classList.remove('error');
    fileDrop.classList.add('edging');
    fileDropTitle.innerHTML = 'Drop to upload!';
}
function fileDefault() {
    const fileDrop = document.querySelector('.fileDrop-block');
    const fileDropTitle = fileDrop.querySelector('.status');

    fileDrop.classList.remove('error');
    fileDrop.classList.remove('edging');
    fileDropTitle.innerHTML = 'Choose or Drop file';
}

function fileDropHandle(event) {
    event.preventDefault()

    const fileDrop = document.querySelector('.fileDrop-block');
    const fileUpload = fileDrop.querySelector('#file');

    fileUpload.files = event.dataTransfer.files;
    
    fileDefault();
    fileChanged();
}

function fileChanged() {
    const dropBlock = document.querySelector('.fileDrop-block');
    const dropBlockStatus = dropBlock.querySelector('.status');
    const dropBlockInput = dropBlock.querySelector('#file');

    if (dropBlockInput.value !== "") {
        dropBlock.classList.add('active');
        dropBlockStatus.innerHTML = dropBlockInput.files[0].name;
    } else {
        fileDefault();
    }
}

function clearUpload() {
    const fileDrop = document.querySelector('#uploadForm');

    const fileUpload = fileDrop.querySelector('#file');
    const fileAlt = fileDrop.querySelector('#alt');
    const fileDescription = fileDrop.querySelector('#description');
    const fileTags = fileDrop.querySelector('#tags');

    fileUpload.value = "";
    fileAlt.value = "";
    fileDescription.value = "";
    fileTags.value = "";
}


// function createJob(file) {
//     jobContainer = document.createElement("div");
//     jobContainer.classList.add("job");

//     jobStatus = document.createElement("span");
//     jobStatus.classList.add("job__status");
//     jobStatus.innerHTML = "Uploading...";

//     jobProgress = document.createElement("span");
//     jobProgress.classList.add("progress");

//     jobImg = document.createElement("img");
//     jobImg.src = URL.createObjectURL(file);

//     jobImgFilter = document.createElement("span");
//     jobImgFilter.classList.add("img-filter");

//     jobContainer.appendChild(jobStatus);
//     jobContainer.appendChild(jobProgress);
//     jobContainer.appendChild(jobImg);
//     jobContainer.appendChild(jobImgFilter);
    
//     return jobContainer;
// }


document.addEventListener('DOMContentLoaded', () => {
    // Function to upload images
    const uploadTab = document.querySelector(".upload-panel");

    if (!uploadTab) { return; } // If upload tab doesn't exist, don't run this code :3

    const uploadTabDrag = uploadTab.querySelector("#dragIndicator");
    const uploadForm = uploadTab.querySelector('#uploadForm');
    // let jobList = document.querySelector(".upload-jobs");
    
    const fileDrop = uploadForm.querySelector('.fileDrop-block');
    const fileDropTitle = fileDrop.querySelector('.status');
    const fileUpload = fileDrop.querySelector('#file');

    const fileAlt = uploadForm.querySelector('#alt');
    const fileDescription = uploadForm.querySelector('#description');
    const fileTags = uploadForm.querySelector('#tags');


    clearUpload();
    fileDefault();

    
    // Tab is dragged
    uploadTabDrag.addEventListener('touchstart', tabDragStart, false);
    uploadTabDrag.addEventListener('touchend', tabDragStopped, false);

    // Drag over/enter event
    fileDrop.addEventListener('dragover', fileActivate, false);
    fileDrop.addEventListener('dragenter', fileActivate, false);
    // Drag out
    fileDrop.addEventListener('dragleave', fileDefault, false);
    // Drop file into box
    fileDrop.addEventListener('drop', fileDropHandle, false);

    // File upload change
    fileUpload.addEventListener('change', fileChanged, false);
    // File upload clicked
    fileUpload.addEventListener('click', fileDefault, false);    


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
        const formData = new FormData();

        formData.append("file", fileUpload.files[0]);
        formData.append("alt", fileAlt.value);
        formData.append("description", fileDescription.value);
        formData.append("tags", fileTags.value);

        // jobItem = createJob(fileUpload.files[0]);
        // jobStatus = jobItem.querySelector(".job__status");

        // Upload the information
        // $.ajax({
        //     url: '/api/upload',
        //     type: 'post',
        //     data: formData,
        //     contentType: false,
        //     processData: false,
        //     beforeSend: function () {
        //         // Add job to list
        //         jobList.appendChild(jobItem);
        //     },
        //     success: function (response) {
        //         jobItem.classList.add("success");
        //         jobStatus.innerHTML = "Uploaded successfully";
        //         if (!document.querySelector(".upload-panel").classList.contains("open")) {
        //             addNotification("Image uploaded successfully", 1);
        //         }
        //     },
        //     error: function (response) {
        //         jobItem.classList.add("critical");
        //         switch (response.status) {
        //             case 500:
        //                 jobStatus.innerHTML = "Server exploded, F's in chat";
        //                 break;
        //             case 400:
        //             case 404:
        //                 jobStatus.innerHTML = "Error uploading. Blame yourself";
        //                 break;
        //             case 403:
        //                 jobStatus.innerHTML = "None but devils play past here...";
        //                 break;
        //             case 413:
        //                 jobStatus.innerHTML = "File too large!!!!!!";
        //                 break;
        //             default:
        //                 jobStatus.innerHTML = "Error uploading file, blame someone";
        //                 break;
        //         }
        //         if (!document.querySelector(".upload-panel").classList.contains("open")) {
        //             addNotification("Error uploading file", 2);
        //         }
        //     },
        // });


        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        // .then(response => response.json())
        .then(data => { addNotification("Image uploaded successfully", 1); })
        .catch(error => {
            switch (response.status) {
                case 500:
                    addNotification("Server exploded, F's in chat", 2)
                    break;
                case 400:
                case 404:
                    addNotification("Error uploading. Blame yourself", 2)
                    break;
                case 403:
                    addNotification("None but devils play past here...", 2)
                    break;
                case 413:
                    addNotification("File too large!!!!!!", 2);
                    break;
                default:
                    addNotification("Error uploading file, blame someone", 2)
                    break;
            }
        });


        clearUpload();
        
        // Reset drop
        fileDrop.classList.remove('active');
        fileDropTitle.innerHTML = 'Choose or Drop file';
    });
});
