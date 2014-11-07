"""
settings.py

Configuration for Flask app

"""


class Config(object):
    # Set secret key to use session
    SECRET_KEY = "likelion-flaskr-secret-key"
    debug = False


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "hmp0077@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///branchers?instance=branchersbeta:branchers'
    migration_directory = 'migrations'

    #
    # oauth
    #
    GOOGLE_CLIENT_ID = "620522363804-0fl954ll60vtb9qjehtoqpff7scahir8.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "lg-wpYghIdasEG4Wbhmw3y9a"

    FACEBOOK_APP_ID = "586906198087470"
    FACEBOOK_APP_SECRET = "268973e56c29610c071c5ad2cc375e79"

    TWITTER_APP_KEY = "e7oK5A8bMNo40L4JzJlkr3bua"
    TWITTER_APP_SECRET = "hkNVX7x68AEd2UUSpxxEno3tFq3k4Vxy5LEqEpz4JXfT2tbKU1"