"""
OnlyLegs - Setup
Runs when the app detects that there is no user directory
"""
import os
import sys
import platformdirs
import logging
import yaml
import re


USER_DIR = platformdirs.user_config_dir('onlylegs')


class Configuration:
    """
    Setup the application on first run
    """
    def __init__(self, verbose=False):
        """
        Main setup function
        """
        if verbose:
            print("Running startup checks...")
        
        # Check if the user directory exists
        if not os.path.exists(USER_DIR):
            self.make_dir()
            
        # Check if the .env file exists
        if not os.path.exists(os.path.join(USER_DIR, '.env')):
            self.make_env()
            
        # Check if the conf.yml file exists
        if not os.path.exists(os.path.join(USER_DIR, 'conf.yml')):
            self.make_yaml()
        
        # Load the config files
        self.logging_config()

    @staticmethod
    def make_dir():
        """
        Create the user directory
        """
        try:
            os.makedirs(USER_DIR)
            os.makedirs(os.path.join(USER_DIR, 'instance'))
        except Exception as err:
            print("Error creating user directory:", err)
            sys.exit(1)
        
        print("Created user directory at:", USER_DIR)

    @staticmethod
    def make_env():
        """
        Create the .env file with default values
        """
        env_conf = {
            'FLASK_SECRET': os.urandom(32).hex(),
        }
        
        try:
            with open(os.path.join(USER_DIR, '.env'), encoding='utf-8', mode='w+') as file:
                for key, value in env_conf.items():
                    file.write(f"{key}={value}\n")
        except Exception as err:
            print("Error creating environment variables:", err)
            sys.exit(1)
        
        print("""
              ####################################################
              # PLEASE NOTE DOWN THE FLASK_SECRET KEY LOCARED IN #
              # YOUR .config/onlylegs/.env FILE! A NEW KEY WAS   #
              # GENERATED FOR YOU!                               #
              ####################################################
              """)

    @staticmethod
    def make_yaml():
        """
        Create the YAML config file with default values
        """
        is_correct = False
        email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        username_regex = re.compile(r'\b[A-Za-z0-9._%+-]+\b')
        
        print("No config file found, please enter the following information:")
        while not is_correct:            
            try:
                username = input("Admin username: ")
                name = input("Admin name: ")
                email = input("Admin email: ")
            except ValueError:
                print("Please enter valid values!")

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
            _ = input("Is this correct? (y/n): ")
            
            if _ == 'y' or _ == 'Y':
                is_correct = True
        
        yaml_conf = {
            'admin': {
                'name': '%s' % name,
                'username': '%s' % username,
                'email': '%s' % email,
            },
            'upload': {
                'allowed-extensions': {
                    'jpg': 'jpeg',
                    'jpeg': 'jpeg',
                    'png': 'png',
                    'webp': 'webp',
                },
                'max-size': 69,
                'rename': 'GWA_{{username}}_{{time}}',
            },
            'website': {
                'name': 'OnlyLegs',
                'motto': 'A gallery built for fast and simple image management. You can change this in the settings',
                'language': 'en',
            }
        }
        
        try:
            with open(os.path.join(USER_DIR, 'conf.yml'), encoding='utf-8', mode='w+') as file:
                yaml.dump(yaml_conf, file, default_flow_style=False)
        except Exception as err:
            print("Error creating default gallery config:", err)
            sys.exit(1)

        print("Generated config file, you can change these values in the settings of the app")

    @staticmethod
    def logging_config():
        logs_path = os.path.join(platformdirs.user_config_dir('onlylegs'), 'logs')

        if not os.path.isdir(logs_path):
            os.mkdir(logs_path)
            print("Created logs directory at:", logs_path)

        logging.getLogger('werkzeug').disabled = True
        logging.basicConfig(
            filename=os.path.join(logs_path, 'only.log'),
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
            encoding='utf-8')