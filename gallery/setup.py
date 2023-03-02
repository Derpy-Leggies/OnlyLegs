# Import dependencies
import platformdirs
import os
import yaml

class setup:
    def __init__(self):
        self.user_dir = platformdirs.user_config_dir('onlylegs')

        print("Running setup...")
        
        if not os.path.exists(self.user_dir):
            self.make_dir()
        if not os.path.exists(os.path.join(self.user_dir, '.env')):
            self.make_env()
        if not os.path.exists(os.path.join(self.user_dir, 'conf.yml')):
            self.make_yaml()
        
    def make_dir(self):
        try:
            os.makedirs(self.user_dir)
            os.makedirs(os.path.join(self.user_dir, 'instance'))
            
            print("Created user directory at:", self.user_dir)
        except Exception as e:
            print("Error creating user directory:", e)
            exit(1) # exit with error code
        
    def make_env(self):
        # Create .env file with default values 
        env_conf = {
            'FLASK_SECRETE': 'dev',
        }
        try:
            with open(os.path.join(self.user_dir, '.env'), 'w') as f:
                for key, value in env_conf.items():
                    f.write(f"{key}={value}\n")
                print("Created environment variables")
        except Exception as e:
            print("Error creating environment variables:", e)
            exit(1)
            
        print("Generated default .env file. EDIT IT BEFORE RUNNING THE APP AGAIN!")
        
    def make_yaml(self):
        # Create yaml config file with default values
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
            with open(os.path.join(self.user_dir, 'conf.yml'), 'w') as f:
                yaml.dump(yaml_conf, f, default_flow_style=False)
                print("Created default gallery config")
        except Exception as e:
            print("Error creating default gallery config:", e)
            exit(1)
            
        print("Generated default YAML config. EDIT IT BEFORE RUNNING THE APP AGAIN!")