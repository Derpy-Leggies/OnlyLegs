// Function to show login
function showLogin() {
    // Create elements
    cancelBtn = document.createElement('button');
    cancelBtn.classList.add('btn-block');
    cancelBtn.classList.add('transparent');
    cancelBtn.innerHTML = 'nuuuuuuuu';
    cancelBtn.onclick = popupDissmiss;

    loginBtn = document.createElement('button');
    loginBtn.classList.add('btn-block');
    loginBtn.classList.add('primary');
    loginBtn.innerHTML = 'Login';
    loginBtn.type = 'submit';
    loginBtn.setAttribute('form', 'loginForm');

    // Create form
    loginForm = document.createElement('form');
    loginForm.id = 'loginForm';
    loginForm.setAttribute('onsubmit', 'return login(event);');

    usernameInput = document.createElement('input');
    usernameInput.classList.add('input-block');
    usernameInput.type = 'text';
    usernameInput.placeholder = 'Namey';
    usernameInput.id = 'username';

    passwordInput = document.createElement('input');
    passwordInput.classList.add('input-block');
    passwordInput.type = 'password';
    passwordInput.placeholder = 'Passywassy';
    passwordInput.id = 'password';

    // Container for remember me checkbox
    rememberMeSpan = document.createElement('span');
    rememberMeSpan.classList.add('input-checkbox');

    rememberMeInput = document.createElement('input');
    rememberMeInput.type = 'checkbox';
    rememberMeInput.id = 'remember-me';

    rememberMeLabel = document.createElement('label');
    rememberMeLabel.innerHTML = 'No forgetty me pls';
    rememberMeLabel.setAttribute('for', 'remember-me');

    rememberMeSpan.appendChild(rememberMeInput);
    rememberMeSpan.appendChild(rememberMeLabel);

    loginForm.appendChild(usernameInput);
    loginForm.appendChild(passwordInput);
    loginForm.appendChild(rememberMeSpan);

    popUpShow(
        'Login!',
        'Need an account? <span class="link" onclick="showRegister()">Register!</span>',
        loginForm,
        [cancelBtn, loginBtn]
    );
}
// Function to login
function login(event) {
    // AJAX takes control of subby form :3
    event.preventDefault();

    let formUsername = document.querySelector("#username").value;
    let formPassword = document.querySelector("#password").value;
    let formRememberMe = document.querySelector("#remember-me").checked;

    if (formUsername === "" || formPassword === "") {
        addNotification("Please fill in all fields!!!!", 3);
        return;
    }

    // Make form
    const formData = new FormData();
    formData.append("username", formUsername);
    formData.append("password", formPassword);
    formData.append("remember-me", formRememberMe);

    fetch('/auth/login', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            location.reload();
        } else {
            if (response.status === 403) {
                addNotification('None but devils play past here... Wrong information', 2);
            } else if (response.status === 500) {
                addNotification('Server exploded, F\'s in chat', 2);
            } else {
                addNotification('Error logging in, blame someone', 2);
            }
        }
    }).catch(error => {
        addNotification('Error logging in, blame someone', 2);
    });
}
// Function to show register
function showRegister() {
    // Create buttons
    cancelBtn = document.createElement('button');
    cancelBtn.classList.add('btn-block');
    cancelBtn.classList.add('transparent');
    cancelBtn.innerHTML = 'nuuuuuuuu';
    cancelBtn.onclick = popupDissmiss;

    registerBtn = document.createElement('button');
    registerBtn.classList.add('btn-block');
    registerBtn.classList.add('primary');
    registerBtn.innerHTML = 'Register';
    registerBtn.type = 'submit';
    registerBtn.setAttribute('form', 'registerForm');

    // Create form
    registerForm = document.createElement('form');
    registerForm.id = 'registerForm';
    registerForm.setAttribute('onsubmit', 'return register(event);');

    usernameInput = document.createElement('input');
    usernameInput.classList.add('input-block');
    usernameInput.type = 'text';
    usernameInput.placeholder = 'Namey';
    usernameInput.id = 'username';

    emailInput = document.createElement('input');
    emailInput.classList.add('input-block');
    emailInput.type = 'text';
    emailInput.placeholder = 'E mail!';
    emailInput.id = 'email';

    passwordInput = document.createElement('input');
    passwordInput.classList.add('input-block');
    passwordInput.type = 'password';
    passwordInput.placeholder = 'Passywassy';
    passwordInput.id = 'password';

    passwordInputRepeat = document.createElement('input');
    passwordInputRepeat.classList.add('input-block');
    passwordInputRepeat.type = 'password';
    passwordInputRepeat.placeholder = 'Passywassy again!';
    passwordInputRepeat.id = 'password-repeat';

    registerForm.appendChild(usernameInput);
    registerForm.appendChild(emailInput);
    registerForm.appendChild(passwordInput);
    registerForm.appendChild(passwordInputRepeat);
    
    popUpShow(
        'Who are you?',
        'Already have an account? <span class="link" onclick="showLogin()">Login!</span>',
        registerForm,
        [cancelBtn, registerBtn]
    );
}
// Function to register
function register(event) {
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
    const formData = new FormData();
    formData.append("username", formUsername);
    formData.append("email", formEmail);
    formData.append("password", formPassword);
    formData.append("password-repeat", formPasswordRepeat);

    // Send form to server
    fetch('/auth/register', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            addNotification('Registered successfully! Now please login to continue', 1);
            showLogin();
        } else {
            if (response.status === 400) {
                response.json().then(data => {
                    for (let i = 0; i < data.length; i++) {
                        addNotification(data[i], 2);
                    }
                });
            } else if (response.status === 403) {
                addNotification('None but devils play past here... Wrong information', 2);
            } else if (response.status === 500) {
                addNotification('Server exploded, F\'s in chat', 2);
            } else {
                addNotification('Error logging in, blame someone', 2);
            }
        }
    }).catch(error => {
        addNotification('Error logging in, blame someone', 2);
    });
}
