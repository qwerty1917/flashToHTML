# -*- coding: utf-8 -*-
"""
Initialize Flask app

"""
from flask.ext.login import LoginManager
from flask import Flask
from flask.ext.oauthlib.client import OAuth
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.signals import Namespace
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask('apps')
app.config.from_object('apps.settings.Production')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You need to login.'

app_signals = Namespace()

# open auth
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_CLIENT_ID'),
    consumer_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
facebook = oauth.remote_app(
    'facebook',
    consumer_key=app.config.get('FACEBOOK_APP_ID'),
    consumer_secret=app.config.get('FACEBOOK_APP_SECRET'),
    request_token_params={
        'scope': ['email', 'public_profile']
    },
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
)
twitter = oauth.remote_app(
    'twitter',
    consumer_key=app.config.get('TWITTER_APP_KEY'),
    consumer_secret=app.config.get('TWITTER_APP_SECRET'),
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

import controllers, models, receivers