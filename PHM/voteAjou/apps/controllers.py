# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from flask.json import jsonify
from flask import render_template, request, redirect, url_for, flash, make_response, g, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from google.appengine.api import images
import requests
from werkzeug.http import parse_options_header
from sqlalchemy import desc
from apps import app, db, login_manager, google, facebook, twitter
from google.appengine.ext import blobstore
from core import variables, OAuthManagement
from werkzeug import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from apps.models import *
from apps.forms import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

@login_manager.unauthorized_handler
def unauthorized():
    message = "login required"
    return redirect(url_for('intro', message=message))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

# @app.befor_request
# def beforRequest():
#     g.userEmail = None
#     g.userName = None
#     if 'userEmail' in session:
#         g.userEmail = session['userEmail']
#         g.userName = session['userName']

@app.route('/', methods=['GET', 'POST'])
def intro(message=None):
    signupForm = SignupForm()
    loginForm = LoginForm()
    if request.method == 'POST':
        # request.args['flag']가 'signup' 이면 실행
        if request.form['flag'] == 'signup':
            if signupForm.validate():

                # 입력된 정보대로 가입
                user = User(
                    userEmail=signupForm.userEmail.data,
                    userName=signupForm.userName.data,
                    password=generate_password_hash(signupForm.password.data),
                    Authority=variables.USER_ROLES['USER'],
                    UserState=variables.USER_STATES['NORMAL']
                )

                db.session.add(user)
                db.session.commit()

                session.permanent = True
                session['userEmail'] = signupForm.userEmail.data
                session['userName'] = signupForm.userName.data

                return redirect(url_for('main'))
            else:
                #입력된 로그인 정보의 폼이 유효하지 않을때
                return render_template('intro.html', signupForm=signupForm, loginForm=loginForm, flag='signup')

        elif request.form['flag'] == 'login':
            if loginForm.validate_on_submit():
                # 입력된 정보대로 로그인
                # blah blah blah
                userEmail = loginForm.userEmail.data
                password = loginForm.password.data

                user = User.query.filter_by(userEmail=userEmail).first()

                if user is None:
                    message = "User not exist."
                elif not check_password_hash(user.password, password):
                    message = "Password invalid."
                else:
                    login_user(user)
                    session.permanent = False
                    # session['userEmail'] = user.userEmail
                    # session['userName'] = user.userName

                    return redirect(request.args.get("next") or url_for("main"))
                #user 가 없거나 pw 불일치일때
                return render_template('intro.html', message=message, signupForm=signupForm, loginForm=loginForm,
                                       flag='login')
            else:
                #입력된 로그인 정보가 유효하지 않을때
                return render_template('intro.html', signupForm=signupForm, loginForm=loginForm, flag='login')
        else:
            # flag가 정의되지 않았을때. 특수한 에러상황임.
            message = "undefined flag"
            return render_template('intro.html', message=message, signupForm=signupForm, loginForm=loginForm,
                                   flag='login')
    else:
        # 최초로 보여지는 인트로 페이지
        return render_template('intro.html', message=message, signupForm=signupForm, loginForm=loginForm, flag='login')

#
############### login by google
#

@app.route('/login/google')
def login_google():
    callback = url_for(
        'google_authorized',
        _external=True
    )
    return google.authorize(callback=callback)

@app.route('/login/google/authorized')
@google.authorized_handler
def google_authorized(resp):
    if resp is None:
        message="Failed to login google"
        return redirect(url_for('intro', message=message))

    logging.info(resp)

    session['google_token'] = (resp['access_token'], '')
    userinfo = google.get('userinfo')

    register_result = OAuthManagement.OAuth2RegisterToUser(userinfo.data, 'GOOGLE')
    return OAuthManagement.OAuthRegisterAndLoginRedirect(register_result)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

#
############### login by facebook
#

@app.route('/login/facebook')
def login_facebook():
    callback = url_for(
        'facebook_authorized',
        _external=True
    )
    return facebook.authorize(callback=callback)

@app.route('/login/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        message="Failed to login facebook"
        return redirect(url_for('intro', message=message))

    logging.info(resp)

    session['oauth_token'] = (resp['access_token'], '')
    userinfo = facebook.get('/me')

    register_result = OAuthManagement.OAuth2RegisterToUser(userinfo.data, 'FACEBOOK')
    return OAuthManagement.OAuthRegisterAndLoginRedirect(register_result)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

#
############### login by twitter
#

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@app.route('/login/twitter')
def login_twitter():
    callback_url = url_for('twitter_authorized')
    return twitter.authorize(callback=callback_url)

@app.route('/login/twitter/authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    session['twitter_oauth'] = resp

    userinfo = twitter.get('account/verify_credentials.json')

    logging.info("Twitter Userinfo")
    logging.info(userinfo.data)

    register_result = OAuthManagement.OAuth2RegisterToUser(userinfo.data, 'TWITTER')
    return OAuthManagement.OAuthRegisterAndLoginRedirect(register_result)

############# logout

@app.route('/logout')
@login_required
def logout():
    logout_user()
    OAuthManagement.OAuthSessionPop()
    return redirect(url_for('intro'))

#
#############
#

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     loginForm = loginForm()
#     if loginForm.validate_on_submit():
#         # login and validate the user...
#         userEmail = loginForm.userEmail.data
#         user = User.query.filter_by(userEmail=userEmail).first()
#         if check_password_hash(user.password, password):
#             login_user(user)
#             flash("Logged in successfully.")
#             return redirect(request.args.get("next") or url_for("main"))
#         else:
#             flash("Password not correct.")
#             return redirect(request.args.get("next") or url_for("intro"))
#     return render_template("intro.html", signupForm=signupForm, loginForm=loginForm, flag='login')

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    #
    # if g.userEmail == None:
    #     message='Please use after login'
    #     return render_template('intro.html', signupForm=signupForm, loginForm=loginForm, flag='login', message=message)
    # else:
        #에디터스 초이스 리스트 만들고 조회순 정렬
    editorsChoicesBranch = Branch.query.order_by(desc(Branch.createDateTime)).filter_by(editorChoice=True)
    editorsChoicesStream = Stream.query.order_by(desc(Stream.createDateTime)).filter_by(editorChoice=True)

    editorsChoices=list(editorsChoicesBranch)+list(editorsChoicesStream)
    editorsChoices.sort(key=lambda x: x.viewCount)

    # What's now 리스트 만들고 최신순 정렬
    newBranches=Branch.query.order_by(desc(Branch.createDateTime)).offset(0).limit(3)
    newStreams=Stream.query.order_by(desc(Stream.createDateTime)).offset(0).limit(3)

    whatsNew=list(newBranches)+list(newStreams)
    whatsNew.sort(key=lambda x: x.createDateTime, reverse=True)
    whatsNew = whatsNew[0:3]

    message=None
    return render_template('main.html', editorsChoices=editorsChoices, whatsNew=whatsNew, message=message)

