"""
Gallery configuration file
"""
import os
import platformdirs
from dotenv import load_dotenv
from yaml import safe_load


# Set dirs
user_dir = platformdirs.user_config_dir("onlylegs")
instance_dir = os.path.join(user_dir, "instance")

# Load environment variables
print("Loading environment variables...")
load_dotenv(os.path.join(user_dir, ".env"))

# Load config from user dir
print("Loading config...")
with open(os.path.join(user_dir, "conf.yml"), encoding="utf-8", mode="r") as file:
    conf = safe_load(file)


# Flask config
SECRET_KEY = os.environ.get("FLASK_SECRET")
SQLALCHEMY_DATABASE_URI = "sqlite:///gallery.sqlite3"

# Upload config
MAX_CONTENT_LENGTH = 1024 * 1024 * conf["upload"]["max-size"]
UPLOAD_FOLDER = os.path.join(user_dir, "uploads")
ALLOWED_EXTENSIONS = conf["upload"]["allowed-extensions"]

# Pass YAML config to app
ADMIN_CONF = conf["admin"]
UPLOAD_CONF = conf["upload"]
WEBSITE_CONF = conf["website"]
