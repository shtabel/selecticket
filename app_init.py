from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = None
db = None


def getApp():
    global app, db
    if not app:
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = config.Config.get_db_uri()
        db = SQLAlchemy(app)

getApp()

