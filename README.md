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
### Currently implemented
- Easy uploading and managing of a gallery of images
- Multi user support, helping you manage a whole group of photographers
- Custom CSS support

### Coming soon tm
- Image groups, helping you sort your favorite memories
- Password locked images/image groups, helping you share photos only to those who you want to
- Logging and automatic login attempt warnings and timeouts
- Searching through tags, file names, users (and metadata maybe, no promises)

## screenshots

Homescreen
![screenshot](.github/images/homepage.png)

Image view
![screenshot](.github/images/imageview.png)

## Running
By default, the app runs on port 5000 with 4 workers, you can pass in arguments to change that, use `-h` or `--help` to see all the options.

Once you clone the repo to your desired location and have installed python `poetry`, install the requirements with `poetry install`. From there you can run the app with Gunicorn using `poetry run python3 run.py`!

You can also run the app in debug mode using `-d` or `--debug`, but its best to look into the logs file located under `~/.config/onlylegs/only.log`

Enjoy using OnlyLegs!