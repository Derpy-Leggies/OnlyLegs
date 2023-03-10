// fade in images
function imgFade(obj, time = 250) {
    $(obj).animate({ opacity: 1 }, time);
}
// https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
function colourContrast(bgColor, lightColor, darkColor, threshold = 0.179) {
    var color = (bgColor.charAt(0) === '#') ? bgColor.substring(1, 7) : bgColor;
    var r = parseInt(color.substring(0, 2), 16); // hexToR
    var g = parseInt(color.substring(2, 4), 16); // hexToG
    var b = parseInt(color.substring(4, 6), 16); // hexToB
    var uicolors = [r / 255, g / 255, b / 255];
    var c = uicolors.map((col) => {
        if (col <= 0.03928) {
            return col / 12.92;
        }
        return Math.pow((col + 0.055) / 1.055, 2.4);
    });
    var L = (0.2126 * c[0]) + (0.7152 * c[1]) + (0.0722 * c[2]);
    return (L > threshold) ? darkColor : lightColor;
}
// Lazy load images when they are in view
function loadOnView() {
    let lazyLoad = document.querySelectorAll('#lazy-load');

    for (let i = 0; i < lazyLoad.length; i++) {
        let image = lazyLoad[i];
        if (image.getBoundingClientRect().top < window.innerHeight && image.getBoundingClientRect().bottom > 0) {
            if (!image.src) {
                image.src = `/api/uploads/${image.getAttribute('data-src')}?w=400&h=400`
            }
        }
    }
}
// Function to upload images
function uploadFile() {
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
        $("#file").val("");
        $("#alt").val("");
        $("#description").val("");
        $("#tags").val("");
    }
};
// open upload tab
function openUploadTab() {
    // Stop scrolling
    document.querySelector("html").style.overflow = "hidden";

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
// Function to show login
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
// Function to login
function login(event) {
    // AJAX takes control of subby form :3
    event.preventDefault();

    let formUsername = document.querySelector("#username").value;
    let formPassword = document.querySelector("#password").value;

    if (formUsername === "" || formPassword === "") {
        addNotification("Please fill in all fields!!!!", 3);
        return;
    }

    // Make form
    var formData = new FormData();
    formData.append("username", formUsername);
    formData.append("password", formPassword);

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
// Function to show register
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
// Function to register
function register(obj) {
    // AJAX takes control of subby form
    event.preventDefault();

    let formUsername = document.querySelector("#username").value;
    let formEmail = document.querySelector("#email").value;
    let formPassword = document.querySelector("#password").value;
    let formPasswordRepeat = document.querySelector("#password-repeat").value;

    if (formUsername === "" || formEmail === "" || formPassword === "" || formPasswordRepeat === "") {
        addNotification("Please fill in all fields!!!!", 3);
        return;
    }

    // Make form
    var formData = new FormData();
    formData.append("username", formUsername);
    formData.append("email", formEmail);
    formData.append("password", formPassword);
    formData.append("password-repeat", formPasswordRepeat);

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

window.onload = function () {
    loadOnView();

    const darkColor = '#151515';
    const lightColor = '#E8E3E3';
    let contrastCheck = document.querySelectorAll('#contrast-check');
    for (let i = 0; i < contrastCheck.length; i++) {
        bgColor = contrastCheck[i].getAttribute('data-color');
        contrastCheck[i].style.color = colourContrast(bgColor, lightColor, darkColor, 0.9);
    }

    let times = document.querySelectorAll('.time');
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
};
window.onscroll = function () {
    loadOnView();

    // Jump to top button
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 20) {
        document.querySelector('.jumpUp').classList = 'jumpUp jumpUp--show';
    } else {
        document.querySelector('.jumpUp').classList = 'jumpUp';
    }
    document.querySelector('.jumpUp').onclick = function () {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
};
window.onresize = function () {
    loadOnView();
};