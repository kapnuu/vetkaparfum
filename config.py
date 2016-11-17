import os


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False

    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    database_uri = os.environ.get('DATABASE_URL')
    if database_uri is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = database_uri

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
