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
Currently only for reference

    poetry install
    poetry run python3 -m flask --app gallery --debug run --host 0.0.0.0
    poetry run python3 -m gunicorn -w 4 -b 0.0.0.0:5000 'gallery:create_app()'