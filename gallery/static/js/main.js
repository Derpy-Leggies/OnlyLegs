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
    // Stop scrolling
    document.querySelector("html").style.overflow = "hidden";

    // Open upload tab
    const uploadTab = document.querySelector(".upload-panel");
    uploadTab.style.display = "block";

    setTimeout( function() {
        uploadTab.classList.add("open");
    }, 10);
}

function closeUploadTab() {
    // un-Stop scrolling
    document.querySelector("html").style.overflow = "auto";

    // Close upload tab
    const uploadTab = document.querySelector(".upload-panel");
    uploadTab.classList.remove("open");

    setTimeout( function() {
        uploadTab.style.display = "none";
    }, 250);
}

function toggleUploadTab() {
    if (document.querySelector(".upload-panel").classList.contains("open")) {
        closeUploadTab();
    } else {
        openUploadTab();
    }
}

function showLogin() {
    popUpShow(
        'idk what to put here, just login please',
        'Need an account? <span class="pop-up__link" onclick="showRegister()">Register!</span>',
        '<button class="pop-up__btn pop-up__btn-primary-fill" form="loginForm" type="submit">Login</button>',
        '<form id="loginForm"  onsubmit="return login(event)">\
            <input class="pop-up__input" type="text" placeholder="Namey" id="username"/>\
            <input class="pop-up__input" type="password" placeholder="Passywassy" id="password"/>\
        </form>'
    );
};
function showRegister() {
    popUpShow(
        'Who are you?',
        'Already have an account? <span class="pop-up__link" onclick="showLogin()">Login!</span>',
        '<button class="pop-up__btn pop-up__btn-primary-fill" form="registerForm" type="submit">Register</button>',
        '<form id="registerForm" onsubmit="return register(event)">\
            <input class="pop-up__input" type="text" placeholder="Namey" id="username"/>\
            <input class="pop-up__input" type="text" placeholder="E mail!" id="email"/>\
            <input class="pop-up__input" type="password" placeholder="Passywassy" id="password"/>\
            <input class="pop-up__input" type="password" placeholder="Passywassy again!" id="password-repeat"/>\
        </form>'
    );
};

function login(event) {
    // AJAX takes control of subby form
    event.preventDefault();

    if ($("#username").val() === "" || $("#password").val() === "") {
        addNotification("Please fill in all fields", 3);
    } else {
        // Make form
        var formData = new FormData();
        formData.append("username", $("#username").val());
        formData.append("password", $("#password").val());

        $.ajax({
            url: '/auth/login',
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                location.reload();
            },
            error: function (response) {
                switch (response.status) {
                    case 500:
                        addNotification('Server exploded, F\'s in chat', 2);
                        break;
                    case 403:
                        addNotification('None but devils play past here... Wrong information', 2);
                        break;
                    default:
                        addNotification('Error logging in, blame someone', 2);
                        break;
                }
            }
        });
    }
}
function register(obj) {
    // AJAX takes control of subby form
    event.preventDefault();

    if ($("#username").val() === "" || $("#email").val() === "" || $("#password").val() === "" || $("#password-repeat").val() === "") {
        addNotification("Please fill in all fields", 3);
    } else {
        // Make form
        var formData = new FormData();
        formData.append("username", $("#username").val());
        formData.append("email", $("#email").val());
        formData.append("password", $("#password").val());
        formData.append("password-repeat", $("#password-repeat").val());

        $.ajax({
            url: '/auth/register',
            type: 'post',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response === "gwa gwa") {
                    addNotification('Registered successfully! Now please login to continue', 1);
                    showLogin();
                } else {
                    for (var i = 0; i < response.length; i++) {
                        addNotification(response[i], 2);
                    }
                }
            },
            error: function (response) {
                switch (response.status) {
                    case 500:
                        addNotification('Server exploded, F\'s in chat', 2);
                        break;
                    case 403:
                        addNotification('None but devils play past here...', 2);
                        break;
                    default:
                        addNotification('Error logging in, blame someone', 2);
                        break;
                }
            }
        });
    }
}
