# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField
)
from wtforms import validators
from wtforms.fields.html5 import EmailField
class SignupForm(Form):
    userEmail = StringField(
        'Email',
        [validators.data_required('Input your Email address.'),
         validators.Email('Your Email format seems wrong.'),
         validators.Length(max=225, message='Too long email address')],
        description="Email address."
    )

    userName = StringField(
        'Username',
        [validators.data_required('Input Username'),
         validators.Length(max=225, message='Too long username')],
        # 서버단에 유저네임 안겹치게 조치 하기
        description='Username'
    )

    password = PasswordField(
        'Password',
        [validators.data_required('Input Password'),
         validators.Length(min=8, max=225, message='Too short password')],
        description='Password'
    )

    passwordConfirm = PasswordField(
        'PasswordConfirm',
        [validators.data_required('Input Password Confirm'),
         validators.EqualTo('password', message='Passwords must match')],
        description='Password Confirm'
    )

class LoginForm(Form):
    userEmail = StringField(
        'Email',
        [validators.data_required('Input your account Email address.'),
         validators.Email('Email format seems wrong.')],
        description= 'Email'
    )

    password = PasswordField(
        'Password',
        [validators.data_required('Input your password'),
         validators.Length(min=8, max=225, message='Password length should be within 8~225')],
        description= 'Password'
    )




# 예전것들
class ArticleForm(Form):
    title = StringField(
        u'제목',
        [validators.data_required(u'제목을 입력하시기 바랍니다.')],
        description={'placeholder': u'제목을 입력하세요.'}
    )
    content = TextAreaField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )
    category = StringField(
        u'카테고리',
        [validators.data_required(u'카테고리를 입력하시기 바랍니다.')],
        description={'placeholder': u'카테고리를 입력하세요.'}
    )

class CommentForm(Form):
    content = StringField(
        u'내용',
        [validators.data_required(u'내용을 입력하시기 바랍니다.')],
        description={'placeholder': u'내용을 입력하세요.'}
    )
    author = StringField(
        u'작성자',
        [validators.data_required(u'이름을 입력하시기 바랍니다.')],
        description={'placeholder': u'이름을 입력하세요.'}
    )
    password = PasswordField(
        u'비밀번호',
        [validators.data_required(u'비밀번호를 입력하시기 바랍니다.')],
        description={'placeholder': u'비밀번호를 입력하세요.'}
    )
    email = EmailField(
        u'이메일',
        [validators.data_required(u'이메일을 입력하시기 바랍니다.')],
        description={'placeholder': u'이메일을 입력하세요.'}
    )