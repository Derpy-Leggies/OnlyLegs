"""
OnlyLegs - Setup
Runs when the app detects that there is no user directory
"""
import os
import re
import platformdirs
import yaml


APPLICATION_ROOT = platformdirs.user_config_dir("onlylegs")
REQUIRED_DIRS = {
    "root": APPLICATION_ROOT,
    "instance": os.path.join(APPLICATION_ROOT, "instance"),
    "media": os.path.join(APPLICATION_ROOT, "media"),
    "uploads": os.path.join(APPLICATION_ROOT, "media", "uploads"),
    "cache": os.path.join(APPLICATION_ROOT, "media", "cache"),
    "pfp": os.path.join(APPLICATION_ROOT, "media", "pfp"),
    "banner": os.path.join(APPLICATION_ROOT, "media", "banner"),
}

EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
USERNAME_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+\b")


def check_dirs():
    """
    Create the user directory
    """

    for directory in REQUIRED_DIRS.values():
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Created directory at:", directory)
        print("User directory already exists at:", directory)


def check_env():
    """
    Create the .env file with default values
    """
    if os.path.exists(os.path.join(APPLICATION_ROOT, ".env")):
        print("Environment file already exists at:", APPLICATION_ROOT)
        return

    env_conf = {
        "FLASK_SECRET": os.urandom(32).hex(),
    }

    with open(
        os.path.join(APPLICATION_ROOT, ".env"), encoding="utf-8", mode="w+"
    ) as file:
        for key, value in env_conf.items():
            file.write(key + "=" + value + "\n")

    print(
        "####################################################",
        "# A NEW KEY WAS GENERATED FOR YOU! PLEASE NOTE     #",
        "# DOWN THE FLASK_SECRET KEY LOCATED IN YOUR        #",
        "# ~/.config/onlylegs/.env FOLDER! LOOSING THIS KEY #",
        "# WILL RESULT IN YOU BEING UNABLE TO LOG IN!       #",
        "####################################################",
        sep="\n",
    )


def check_conf():
    """
    Create the YAML config file with default values
    """
    if os.path.exists(os.path.join(APPLICATION_ROOT, "conf.yml")):
        print("Config file already exists at:", APPLICATION_ROOT)
        return

    cant_continue = True
    username = "admin"
    name = "Admin"
    email = "admin@example.com"

    print("No config file found, please enter the following information:")
    while cant_continue:
        username = input("Admin username: ").strip()
        name = input("Admin name: ").strip()
        email = input("Admin email: ").strip()

        if not username or not USERNAME_REGEX.match(username):
            print("Username is invalid!")
            continue
        if not name:
            print("Name is invalid!")
            continue
        if not email or not EMAIL_REGEX.match(email):
            print("Email is invalid!")
            continue

        # Check if user is happy with the values
        is_correct = input("Is this correct? (Y/n): ").lower().strip()
        if is_correct == "y" or not is_correct:
            cant_continue = False

    yaml_conf = {
        "admin": {
            "name": name,
            "username": username,
            "email": email,
        },
        "upload": {
            "allowed-extensions": {
                "jpg": "jpeg",
                "jpeg": "jpeg",
                "png": "png",
                "webp": "webp",
            },
            "max-size": 69,
            "max-load": 50,
            "rename": "GWA_{{username}}_{{time}}",
        },
        "website": {
            "name": "OnlyLegs",
            "motto": "A gallery built for fast and simple image management!",
            "language": "en",
        },
    }

    with open(
        os.path.join(APPLICATION_ROOT, "conf.yml"), encoding="utf-8", mode="w+"
    ) as file:
        yaml.dump(yaml_conf, file, default_flow_style=False)

    print(
        "####################################################",
        "# A NEW CONFIG HAS BEEN GENERATED AT:              #",
        "# ~/.config/onlylegs/conf.yml                      #",
        "####################################################",
        sep="\n",
    )
