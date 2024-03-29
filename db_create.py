#!flask/bin/python
from migrate.versioning import api
from config import Config
from vetka import app, db
import os.path

with app.app_context():
    db.create_all()

if not os.path.exists(Config.SQLALCHEMY_MIGRATE_REPO):
    api.create(Config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, api.version(Config.SQLALCHEMY_MIGRATE_REPO))
