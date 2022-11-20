import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

settings = os.environ.get('APP_SETTINGS')
if settings is None:
    settings = 'DevelopConfig'
app.config.from_object('config.' + settings)

db = SQLAlchemy(app)

from vetka import views, models, x_create_db, filters
