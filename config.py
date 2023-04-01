"""Flask configuration."""
import os

FLASK_ENV = os.environ.get("FLASK_ENV", "development")


if FLASK_ENV == "development":
    from os import environ, path
    from dotenv import load_dotenv

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, ".env"))

TESTING = os.environ.get("TESTING")
DEBUG = os.environ.get("DEBUG")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
DATASET_LOCATION = os.environ.get("DATASET_LOCATION")
DATASET_ID = os.environ.get("DATASET_ID")


# Database configuration
POSTGRES = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
    "database": os.environ.get("DB_NAME"),
    "connection_name": os.environ.get("CONNECTION_NAME"),
}

SQLALCHEMY_DATABASE_URI = (
    "postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s" % POSTGRES
)

# For socket based connection
if FLASK_ENV == "staging":
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://%(user)s:%(password)s@/%(database)s?host=%(connection_name)s/"
        % POSTGRES
    )

SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ.get("SECRET_KEY")
RAPID_PRO_AUTHORIZATION_TOKEN = os.environ.get("RAPID_PRO_AUTHORIZATION_TOKEN")
CHURNED_USER_GROUP_NAME = os.environ.get("CHURNED_USER_GROUP_NAME")
RAPID_PRO_API_URL = os.environ.get("RAPID_PRO_API_URL")
