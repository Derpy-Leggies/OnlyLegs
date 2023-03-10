"""
OnlyLegs - Setup
Runs when the app detects that there is no user directory
"""
import os
import sys
import platformdirs
import logging
import yaml

USER_DIR = platformdirs.user_config_dir('onlylegs')

class SetupApp:
    """
    Setup the application on first run
    """
    def __init__(self):
        """
        Main setup function
        """
        print("Running setup...")
        
        self.requires_restart = False

        if not os.path.exists(USER_DIR):
            self.make_dir()
        if not os.path.exists(os.path.join(USER_DIR, '.env')):
            self.make_env()
        if not os.path.exists(os.path.join(USER_DIR, 'conf.yml')):
            self.make_yaml()
            
        self.logging_config()
        
        if self.requires_restart:
            print("WARNING: You need to restart and edit the config files before running the app again!")
            print("You can find the config files at:", USER_DIR)
            sys.exit()

    def make_dir(self):
        """
        Create the user directory
        """
        try:
            os.makedirs(USER_DIR)
            os.makedirs(os.path.join(USER_DIR, 'instance'))

            print("Created user directory at:", USER_DIR)
        except Exception as err:
            print("Error creating user directory:", err)
            sys.exit(1)

    def make_env(self):
        """
        Create the .env file with default values
        """
        env_conf = {
            'FLASK_SECRETE': 'dev',
        }
        try:
            with open(os.path.join(USER_DIR, '.env'), encoding='utf-8') as file:
                for key, value in env_conf.items():
                    file.write(f"{key}={value}\n")
                print("Created environment variables")
        except Exception as err:
            print("Error creating environment variables:", err)
            sys.exit(1)

        print("Generated default .env file, please edit!")

    def make_yaml(self):
        """
        Create the YAML config file with default values
        """
        yaml_conf = {
            'admin': {
                'name': 'Real Person',
                'username': 'User',
                'email': 'real-email@some.place'
            },
            'upload': {
                'allowed-extensions': {
                    'jpg': 'jpeg',
                    'jpeg': 'jpeg',
                    'png': 'png',
                    'webp': 'webp'
                },
                'max-size': 69,
                'rename': 'GWA_\{\{username\}\}_\{\{time\}\}'
            },
            'website': {
                'name': 'OnlyLegs',
                'motto': 'Gwa Gwa',
                'language': 'english'
            },
            'server': {
                'host': '0.0.0.0',
                'port': 5000
            },
        }
        try:
            with open(os.path.join(USER_DIR, 'conf.yml'), encoding='utf-8') as file:
                yaml.dump(yaml_conf, file, default_flow_style=False)
                print("Created default gallery config")
        except Exception as err:
            print("Error creating default gallery config:", err)
            sys.exit(1)

        print("Generated default YAML config, please edit!")

    def logging_config(self):
        LOGS_PATH = os.path.join(platformdirs.user_config_dir('onlylegs'), 'logs')

        if not os.path.isdir(LOGS_PATH):
            os.mkdir(LOGS_PATH)
            print("Created logs directory at:", LOGS_PATH)

        logging.getLogger('werkzeug').disabled = True
        logging.basicConfig(
            filename=os.path.join(LOGS_PATH, 'only.log'),
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
            encoding='utf-8')