import os
# noinspection PyPackageRequirements
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    ENV = os.environ.get('ENV') or 'production'
    DEBUG = os.environ.get('DEBUG') == "True" or False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False

    CACHE_TYPE = "filesystem"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_IGNORE_ERRORS = True
    CACHE_DIR = os.path.join(basedir, "cache")
    CACHE_THRESHOLD = 100

    ODK = False
    SOND = False

# requirements
# pip freeze > requirements.txt
