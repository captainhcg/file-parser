#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + settings.DB_NAME

app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
db = SQLAlchemy(app)



