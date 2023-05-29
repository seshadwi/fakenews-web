import os

# Each Flask web application contains a secret key which used to sign session cookies for protection against cookie data tampering.
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
# basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode, that will refresh the page when you make changes.
DEBUG = True

# Connect to the MYSQL database

HOST = os.environ.get('DB_HOST')
USER = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
NAME = os.environ.get('DB_NAME')

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOST, NAME) if PASSWORD != '' else 'mysql://%s@%s/%s'%(USER, HOST, NAME)

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False