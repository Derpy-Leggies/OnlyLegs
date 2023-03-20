// Function to show login
function showLogin() {
    popUpShow(
        'Login!',
        'Need an account? <span class="pop-up__link" onclick="showRegister()">Register!</span>',
        '<button class="btn-block" onclick="popupDissmiss()">Cancelee</button>\
        <button class="btn-block primary" form="loginForm" type="submit">Login</button>',
        '<form id="loginForm"  onsubmit="return login(event)">\
            <input class="input-block" type="text" placeholder="Namey" id="username"/>\
            <input class="input-block" type="password" placeholder="Passywassy" id="password"/>\
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
        '<button class="btn-block" onclick="popupDissmiss()">Canceleee</button>\
        <button class="btn-block primary" form="registerForm" type="submit">Register</button>',
        '<form id="registerForm" onsubmit="return register(event)">\
            <input class="input-block" type="text" placeholder="Namey" id="username"/>\
            <input class="input-block" type="text" placeholder="E mail!" id="email"/>\
            <input class="input-block" type="password" placeholder="Passywassy" id="password"/>\
            <input class="input-block" type="password" placeholder="Passywassy again!" id="password-repeat"/>\
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