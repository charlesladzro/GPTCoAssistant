import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Load configurations from the "default" section
START_DIR = config.get("default", "START_DIR")
SERVER_URL = f"https://{config.get("default", "SERVER_URL")}"
TITLE = config.get("default", "TITLE")
VERSION = config.get("default", "VERSION")
SECRET_API_KEY = config.get("default", "SECRET_API_KEY")
