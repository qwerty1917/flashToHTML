#-*- coding: utf-8 -*-
"""
models_new.py

"""

from apps import db
from sqlalchemy.orm import deferred, relationship
from core import variables


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(120))
    userName = db.Column(db.String(64))
    profileImage = db.Column(db.String(255))
    password = db.Column(db.String(255))
    Authority = db.Column(db.SmallInteger, default=variables.USER_ROLES['USER']) # 0 = 일반 사용자 1 = 관리자
    UserState = db.Column(db.SmallInteger, default=variables.USER_STATES['NORMAL']) # 0 = 일반 1 = 쓰기제한 2 = 블랙리스트
    createDateTime = db.Column(db.DateTime, default=db.func.now())
    dateLastLoggedIn = db.Column(db.DateTime)

class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    Summary = db. Column(db.String(255))
    viewCount = db.Column(db.Integer, default=0)
    onEditFlag = db.Column(db.Integer)
    editorChoice = db.Column(db.Boolean, default=False)
    createDateTime = db.Column(db.DateTime, default=db.func.now())

    coverImage = db.Column(db.String(255))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('streams', cascade='all, delete-orphan', lazy='dynamic'))

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    Summary = db. Column(db.String(255))
    viewCount = db.Column(db.Integer, default=0)
    onEditFlag = db.Column(db.Integer)
    editorChoice = db.Column(db.Boolean, default=False)
    createDateTime = db.Column(db.DateTime, default=db.func.now())

    coverImage = db.Column(db.String(255))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('branches', cascade='all, delete-orphan', lazy='dynamic'))

    rootCardId = db.Column(db.Integer, db.ForeignKey('card.id'))
    card = db.relationship('Card',
                           backref=db.backref('childBranches'), post_update=True)
    # card = db.relationship('Card',
    #                        backref=db.backref('childBranches', cascade='all, delete-orphan', lazy='dynamic'))

    # 현재 branch 객체가 참조하는 것이
    # stream 일땐 stream 에만 값 할당,
    # branch 일떈 branch 에만 값 할당

    parentBranchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
    parentBranch = db.relation('Branch', remote_side=[id])
    childeBranch = db.relationship("Branch", lazy="joined", join_depth=2)
    # parentBranch = db.relationship('Branch',
    #                                backref=db.backref('childBranches', cascade='all, delete-orphan', lazy='dynamic',))

    parentStreamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
    stream = db.relationship('Stream',
                             backref=db.backref('childBranches', cascade='all, delete-orphan', lazy='dynamic'))

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 현재 card 객체를 포함한 것이
    # stream 일땐 stream 에만 값 할당,
    # branch 일떈 branch 에만 값 할당
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
    branch = db.relationship('Branch', backref=db.backref('cards', cascade='all, delete-orphan', lazy='dynamic'))

    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
    stream = db.relationship('Stream', backref=db.backref('cards', cascade='all, delete-orphan', lazy='dynamic'))

    order = db.Column(db.Float)
    content = db.Column(db.Text)
    createDateTime = db.Column(db.DateTime, default=db.func.now())
    finalEditDateTime = db.Column(db.DateTime)


class StreamTitleKeyword(db.Model):
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'), primary_key=True)
    stream = db.relationship('Stream',
                             backref=db.backref('titleKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))

class StreamContentKeyword(db.Model):
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'), primary_key=True)
    stream = db.relationship('Stream',
                             backref=db.backref('contentKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))


class BranchTitleKeyword(db.Model):
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'), primary_key=True)
    branch = db.relationship('Branch',
                             backref=db.backref('titleKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))


class BranchContentKeyword(db.Model):
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'), primary_key=True)
    branch = db.relationship('Branch',
                             backref=db.backref('contentKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagWord = db.Column(db.String(50))

    StreamTagRelation = db.relationship('Stream', secondary=StreamTagRelation,
                                        backref=db.backref('tags', lazy='dynamic'))

    BranchTagRelation = db.relationship('Branch', secondary=BranchTagRelation,
                                        backref=db.backref('tags', lazy='dynamic'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    cardId = db.Column(db.Integer, db.ForeignKey('card.id'))
    card = db.relationship('Card', backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

    content = db.Column(db.Text())
    createDateTime = db.Column(db.DateTime, default=db.func.now())

    CommentThumbsUp = db.relationship('User', secondary=CommentThumbsUp,
                                        backref=db.backref('commentThumbsUps', lazy='dynamic'))

class StreamTagRelation(db.Model):
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'), primary_key=True)
    stream = db.relationship('Stream', backref=db.backref('tagRelations', cascade='all, delete-orphan', lazy='dynamic'))

    tagId = db.Column(db.String(50), db.ForeignKey('tag.id'), primary_key=True)
    tag = db.relationship('Tag', backref=db.backref('streamRelations', cascade='all, delete-orphan', lazy='dynamic'))

class BranchTagRelation(db.Model):
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'), primary_key=True)
    branch = db.relationship('Branch', backref=db.backref('tagRelations', cascade='all, delete-orphan', lazy='dynamic'))

    tagId = db.Column(db.String(50), db.ForeignKey('tag.id'), primary_key=True)
    tag = db.relationship('Tag', backref=db.backref('branchRelations', cascade='all, delete-orphan', lazy='dynamic'))

class StreamBookMark(db.Model):
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'), primary_key=True)
    stream = db.relationship('Stream', backref=db.backref('bookmarks', cascade='all, delete-orphan', lazy='dynamic'))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('streamBookmarks', cascade='all, delete-orphan', lazy='dynamic'))

    cardId = db.Column(db.Integer, db.ForeignKey('card.id'))
    card = db.relationship('Card', backref=db.backref('streamBookmarks', cascade='all, delete-orphan', lazy='dynamic'))

    createDateTime = db.Column(db.DateTime, default=db.func.now())

class BranchBookMark(db.Model):
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'), primary_key=True)
    branch = db.relationship('Branch', backref=db.backref('bookmarks', cascade='all, delete-orphan', lazy='dynamic'))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('branchBookmarks', cascade='all, delete-orphan', lazy='dynamic'))

    cardId = db.Column(db.Integer, db.ForeignKey('card.id'))
    card = db.relationship('Card', backref=db.backref('branchBookmarks', cascade='all, delete-orphan', lazy='dynamic'))

    createDateTime = db.Column(db.DateTime, default=db.func.now())

class StreamThumbsUp(db.Model):
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'), primary_key=True)
    stream = db.relationship('Stream', backref=db.backref('thumbsUps', cascade='all, delete-orphan', lazy='dynamic'))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('streamThumbsUps', cascade='all, delete-orphan', lazy='dynamic'))

    createDateTime = db.Column(db.DateTime, default=db.func.now())

class BranchThumbsUp(db.Model):
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'), primary_key=True)
    branch = db.relationship('Branch', backref=db.backref('thumbsUps', cascade='all, delete-orphan', lazy='dynamic'))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('branchThumbsUps', cascade='all, delete-orphan', lazy='dynamic'))

    createDateTime = db.Column(db.DateTime, default=db.func.now())

class CommentThumbsUp(db.Model):
    commentId = db.Column(db.Integer, db.ForeignKey('comment.id'), primary_key=True)
    comment = db.relationship('Comment', backref=db.backref('thumbsUps', cascade='all, delete-orphan', lazy='dynamic'))

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('commentThumbsUps', cascade='all, delete-orphan', lazy='dynamic'))

    createDateTime = db.Column(db.DateTime, default=db.func.now())

################# former one #################

# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     content = db.Column(db.Text())
#     author = db.Column(db.String(255))
#     category = db.Column(db.String(255))
#     like = db.Column(db.Integer)
#     date_created = db.Column(db.DateTime, default = db.func.now())
#
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     #class name 'article' will be changed to lower case table name after migration
#     article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
#     article = db.relationship('Article',
#                               backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))
#
#     content = db.Column(db.Text())
#     author = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     password = db.Column(db.String(255))
#     like = db.Column(db.Integer)
#     date_created = db.Column(db.DateTime, default = db.func.now())
