function showLogin() {
    popUpShow(
        'idk what to put here, just login please',
        'Need an account? <span class="pop-up__link" onclick="showRegister()">Register!</span>',
        '',
        '<form onsubmit="return login(event)">\
            <input class="pop-up__input" type="text" placeholder="Namey" id="username"/>\
            <input class="pop-up__input" type="password" placeholder="Passywassy" id="password"/>\
            <button class="pop-up__btn pop-up__btn-primary-fill">Login</button>\
        </form>'
    );
};
function showRegister() {
    popUpShow(
        'Who are you?',
        'Already have an account? <span class="pop-up__link" onclick="showLogin()">Login!</span>',
        '',
        '<form onsubmit="return register(event)">\
            <input class="pop-up__input" type="text" placeholder="Namey" id="username"/>\
            <input class="pop-up__input" type="text" placeholder="E mail!" id="email"/>\
            <input class="pop-up__input" type="password" placeholder="Passywassy" id="password"/>\
            <input class="pop-up__input" type="password" placeholder="Passywassy again!" id="password-repeat"/>\
            <button class="pop-up__btn pop-up__btn-primary-fill">Register</button>\
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