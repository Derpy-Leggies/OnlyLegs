<div align="center">
    <img src=".github/images/OnlyLegs.png" width="200" height="200"/>
    <div id="user-content-toc">
        <ul>
            <summary><h1 style="display: inline-block;">OnlyLegs</h1></summary>
        </ul>
    </div>
    <p>Gallery built for fast and simple image management</p>
</div>
<div align="center">
    <a href="https://git.leggy.dev/Fluffy/onlylegs">
        <img src="https://img.shields.io/badge/Gitea-34495E?style=for-the-badge&logo=gitea&logoColor=5D9425">
    </a>
    <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white">
    <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
    <a href="https://github.com/Fluffy-Bean/onlylegs/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/Fluffy-Bean/onlylegs?style=for-the-badge">
    </a>
    <a href="https://wakatime.com/badge/user/29bd1733-45f0-41c0-901e-d6daf49094d4/project/6aae41df-003f-4b17-ae8f-62cecfb3fc24">
        <img src="https://wakatime.com/badge/user/29bd1733-45f0-41c0-901e-d6daf49094d4/project/6aae41df-003f-4b17-ae8f-62cecfb3fc24.svg?style=for-the-badge" alt="wakatime">
        </a>
</div>

## Features
 - [x] Easy uploading and managing of a gallery of images
 - [x] Multi-user support, helping you manage a whole group of photographers
 - [x] Image groups, helping you sort your favourite memories
 - [x] Custom CSS support
 - [ ] Password locked images/image groups, helping you share photos only to those who you want to
 - [ ] Logging and automatic login attempt warnings and timeouts
 - [ ] Searching through tags, file names and users

And many more planned things!

## screenshots

Home-screen
![screenshot](.github/images/homepage.png)

Image view
![screenshot](.github/images/imageview.png)

## Running

You first need to install `python poetry`, it's best to follow their getting started guide you can find on the official website.

Next we need to install the required packages for the gallery to function correctly, make sure you're in the directory of the project when you run this command:

    poetry install

By default, the app runs on port 5000, 4 workers on `gunicorn` ready for you to use it. You can find more information on this using the `-h` flag. But to run the gallery, use this command.

    poetry run python3 run.py

Now follow the provided prompts to fill in the information for the Admin account, and you're ready to go!

### Common issues
#### App failing to create a user config folder

Try checking if you have `XDG_CONFIG_HOME` setup. If you don't, you can set that with this command:

    export XDG_CONFIG_HOME="$HOME/.config"

## Final notes

Thank you to everyone who helped me test the previous and current versions of the gallery, especially critters:

 - Carty
 - Jeetix
 - CRT
 - mrHDash
 - Verg
 - FennecBitch

Enjoy using OnlyLegs!