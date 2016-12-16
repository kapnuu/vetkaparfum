import os


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False

    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(16)

    database_uri = os.environ.get('DATABASE_URL')
    if database_uri is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = database_uri

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = 'db_repository'

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    ADMIN_SALT = os.environ.get('ADMIN_SALT')

    SENDGRID_API_TOKEN = os.environ.get('SENDGRID_API_TOKEN')
    FEEDBACK_RECEIVER = os.environ.get('FEEDBACK_RECEIVER')
    FEEDBACK_SENDER = os.environ.get('FEEDBACK_SENDER')

    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    FEEDBACK_PHONE_SRC = os.environ.get('FEEDBACK_PHONE_SRC')
    FEEDBACK_PHONE_DST = os.environ.get('FEEDBACK_PHONE_DST')


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
