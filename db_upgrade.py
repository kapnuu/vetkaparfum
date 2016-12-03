#!flask/bin/python
from migrate.versioning import api
from config import Config
print('SQLALCHEMY_DATABASE_URI: % s' % Config.SQLALCHEMY_DATABASE_URI)
print('SQLALCHEMY_MIGRATE_REPO: % s' % Config.SQLALCHEMY_MIGRATE_REPO)
api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
print('Current DB version: ' + str(api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)))
