from flask import session, flash, redirect, url_for
from flask.ext.login import login_user
from apps import db
from apps.models import User
from core import variables


def OAuth2RegisterToUser(user_data, type):
    if type == 'TWITTER':
        user = User.query.filter_by(userEmail=str(user_data.get('screen_name')) + "@twitter.com").first()
    else:
        user = User.query.filter_by(userEmail=user_data.get('email')).first()

    if user is None:
        if type == 'GOOGLE':
            user = User(
                userEmail=user_data['email'],
                userName=user_data['name'],
                profileImage=user_data['picture'],
                Authority=variables.USER_ROLES['USER'],
                UserState=variables.USER_STATES['NORMAL']
            )
            db.session.add(user)
            db.session.commit()

        elif type == 'FACEBOOK':
            user = User(
                userName=user_data['name'],
                userEmail=user_data['email'],
                profileImage="http://graph.facebook.com/%s/picture" % user_data['id'],
                Authority=variables.USER_ROLES['USER'],
                UserState=variables.USER_STATES['NORMAL']
            )
            db.session.add(user)
            db.session.commit()

        elif type == 'TWITTER':
            user = User(
                userName=user_data['name'],
                userEmail=str(user_data['screen_name']) + "@twitter.com",
                profileImage=user_data['profile_image_url'],
                Authority=variables.USER_ROLES['USER'],
                UserState=variables.USER_STATES['NORMAL']
            )
            db.session.add(user)
            db.session.commit()

        #
        # @users
        #
        users = User.query.filter_by(userEmail=user.userEmail)

        if users.count() > 1:
            return 409

        user = users.first()

    if user:
        if login_user(user):
            return 200
        else:
            return 500

def OAuthSessionPop():
    OAUTH_PROVIDER = ['google_token', 'oauth_token', 'twitter_oauth']
    for provider in OAUTH_PROVIDER:
        session.pop(provider, None)

def OAuthRegisterAndLoginRedirect(register_result):
    if register_result == 200:
        flash("login success.", "success")
        return redirect(url_for('main'))
    elif register_result == 409:
        flash("already registered email.", "warning")
        return redirect(url_for('intro'))
    elif register_result == 500:
        flash("register failed. please try again.", "error")
        return redirect(url_for('intro'))