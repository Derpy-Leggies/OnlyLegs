"""
OnlyLegs - Setup
Runs when the app detects that there is no user directory
"""
import os
import logging
import re
import platformdirs
import yaml


USER_DIR = platformdirs.user_config_dir("onlylegs")


class Configuration:
    """
    Setup the application on first run
    """

    def __init__(self):
        """
        Main setup function
        """
        print("Running startup checks...")

        # Check if the user directory exists
        if not os.path.exists(USER_DIR):
            self.make_dir()

        # Check if the .env file exists
        if not os.path.exists(os.path.join(USER_DIR, ".env")):
            self.make_env()

        # Check if the conf.yml file exists
        if not os.path.exists(os.path.join(USER_DIR, "conf.yml")):
            self.make_yaml()

        # Load the config files
        self.logging_config()

    @staticmethod
    def make_dir():
        """
        Create the user directory
        """
        os.makedirs(USER_DIR)
        os.makedirs(os.path.join(USER_DIR, "instance"))
        os.makedirs(os.path.join(USER_DIR, "uploads"))

        print("Created user directory at:", USER_DIR)

    @staticmethod
    def make_env():
        """
        Create the .env file with default values
        """
        env_conf = {
            "FLASK_SECRET": os.urandom(32).hex(),
        }

        with open(os.path.join(USER_DIR, ".env"), encoding="utf-8", mode="w+") as file:
            for key, value in env_conf.items():
                file.write(f"{key}={value}\n")

        print(
            """
####################################################
# A NEW KEY WAS GENERATED FOR YOU! PLEASE NOTE     #
# DOWN THE FLASK_SECRET KEY LOCATED IN YOUR        #
# .config/onlylegs/.env FOLDER! LOOSING THIS KEY   #
# WILL RESULT IN YOU BEING UNABLE TO LOG IN!       #
####################################################
              """
        )

    @staticmethod
    def make_yaml():
        """
        Create the YAML config file with default values
        """
        is_correct = False
        email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        username_regex = re.compile(r"\b[A-Za-z0-9._%+-]+\b")

        print("\nNo config file found, please enter the following information:")
        while not is_correct:
            username = input("Admin username: ")
            name = input("Admin name: ")
            email = input("Admin email: ")

            # Check if the values are valid
            if not username or not username_regex.match(username):
                print("Username is invalid!")
                continue

            if not name:
                print("Name is invalid!")
                continue

            if not email or not email_regex.match(email):
                print("Email is invalid!")
                continue

            # Check if user is happy with the values
            if input("Is this correct? (y/n): ").lower() == "y":
                is_correct = True

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
            os.path.join(USER_DIR, "conf.yml"), encoding="utf-8", mode="w+"
        ) as file:
            yaml.dump(yaml_conf, file, default_flow_style=False)

        print(
            "Generated config file, you can change these values in the settings of the app"
        )

    @staticmethod
    def logging_config():
        """
        Set the logging config
        """
        logging.getLogger("werkzeug").disabled = True
        logging.basicConfig(
            filename=os.path.join(USER_DIR, "only.log"),
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
            encoding="utf-8",
        )
