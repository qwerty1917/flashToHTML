from datetime import datetime
import logging
from flask.ext.login import user_logged_in
from apps import db, app


def user_logged_in_callback(app, user, **extra):
    logging.info("user logged in receiver")
    logging.info(user)
    if user.is_authenticated():
        user.dateLastLoggedIn = datetime.utcnow()
        db.session.add(user)
        db.session.commit()


user_logged_in.connect(user_logged_in_callback, app)