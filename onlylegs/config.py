"""
Gallery configuration file
"""
import os
import platformdirs
import importlib.metadata
from dotenv import load_dotenv
from yaml import safe_load


# Set dirs
user_dir = platformdirs.user_config_dir("onlylegs")
instance_dir = os.path.join(user_dir, "instance")

# Load environment variables
# print("Loading environment variables...")
load_dotenv(os.path.join(user_dir, ".env"))

# Load config from user dir
# print("Loading config...")
with open(os.path.join(user_dir, "conf.yml"), encoding="utf-8", mode="r") as file:
    conf = safe_load(file)


# Flask config
SECRET_KEY = os.environ.get("FLASK_SECRET")
SQLALCHEMY_DATABASE_URI = "sqlite:///gallery.sqlite3"
MAX_CONTENT_LENGTH = 1024 * 1024 * conf["upload"]["max-size"]
ALLOWED_EXTENSIONS = conf["upload"]["allowed-extensions"]

# Pass YAML config to app
ADMIN_CONF = conf["admin"]
UPLOAD_CONF = conf["upload"]
WEBSITE_CONF = conf["website"]

# Directories
UPLOAD_FOLDER = os.path.join(user_dir, "media", "uploads")
CACHE_FOLDER = os.path.join(user_dir, "media", "cache")
PFP_FOLDER = os.path.join(user_dir, "media", "pfp")
MEDIA_FOLDER = os.path.join(user_dir, "media")

# Database
INSTANCE_DIR = instance_dir
MIGRATIONS_DIR = os.path.join(INSTANCE_DIR, "migrations")

# App
APP_VERSION = importlib.metadata.version("OnlyLegs")