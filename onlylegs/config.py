"""
Gallery configuration file
"""
import os
import platformdirs
import importlib.metadata
from dotenv import load_dotenv
from yaml import safe_load
from utils import startup


# App Sanity Checks
startup.check_dirs()
startup.check_env()
startup.check_conf()


# Set dirs
APPLICATION_ROOT = platformdirs.user_config_dir("onlylegs")

# Load environment variables
# print("Loading environment variables...")
load_dotenv(os.path.join(APPLICATION_ROOT, ".env"))

# Load config from user dir
# print("Loading config...")
with open(
    os.path.join(APPLICATION_ROOT, "conf.yml"), encoding="utf-8", mode="r"
) as file:
    conf = safe_load(file)


# Flask config
SECRET_KEY = os.environ.get("FLASK_SECRET")
DATABASE_NAME = "gallery.sqlite3"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_NAME
MAX_CONTENT_LENGTH = 1024 * 1024 * conf["upload"]["max-size"]
ALLOWED_EXTENSIONS = conf["upload"]["allowed-extensions"]

# Pass YAML config to app
ADMIN_CONF = conf["admin"]
UPLOAD_CONF = conf["upload"]
WEBSITE_CONF = conf["website"]

# Directories
UPLOAD_FOLDER = os.path.join(APPLICATION_ROOT, "media", "uploads")
MEDIA_FOLDER = os.path.join(APPLICATION_ROOT, "media")
CACHE_FOLDER = os.path.join(APPLICATION_ROOT, "media", "cache")
PFP_FOLDER = os.path.join(APPLICATION_ROOT, "media", "pfp")
BANNER_FOLDER = os.path.join(APPLICATION_ROOT, "media", "banner")

# Database
INSTANCE_DIR = os.path.join(APPLICATION_ROOT, "instance")
MIGRATIONS_DIR = os.path.join(INSTANCE_DIR, "migrations")

# App
APP_VERSION = importlib.metadata.version("OnlyLegs")
