#-*- coding: utf-8 -*-
"""
models.py

"""

from apps import db
from sqlalchemy.orm import deferred, relationship
from core import variables

StreamBookMark = db.Table('StreamBookMark',
    db.Column('streamId', db.Integer, db.ForeignKey('stream.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('cardId', db.Integer, db.ForeignKey('card.id')),
    db.Column('createDateTime', db.DateTime, default=db.func.now())
)

BranchBookMark = db.Table('BranchBookMark',
    db.Column('branchId', db.Integer, db.ForeignKey('branch.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('cardId', db.Integer, db.ForeignKey('card.id')),
    db.Column('createDateTime', db.DateTime, default=db.func.now())
)

StreamThumbsUp = db.Table('StreamThumbsUp',
    db.Column('streamId', db.Integer, db.ForeignKey('stream.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('createDateTime', db.DateTime, default=db.func.now())
)

BranchThumbsUp = db.Table('BranchThumbsUp',
    db.Column('branchId', db.Integer, db.ForeignKey('branch.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('createDateTime', db.DateTime, default=db.func.now())
)

CommentThumbsUp = db.Table('CommentThumbsUp',
    db.Column('commentId', db.Integer, db.ForeignKey('comment.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('createDateTime', db.DateTime, default=db.func.now())
)

StreamTagRelation = db.Table('StreamTagRelation',
    db.Column('streamId', db.Integer, db.ForeignKey('stream.id')),
    db.Column('tagId', db.Integer, db.ForeignKey('tag.id'))
)

BranchTagRelation = db.Table('BranchTagRelation',
    db.Column('branchId', db.Integer, db.ForeignKey('branch.id')),
    db.Column('tagId', db.Integer, db.ForeignKey('tag.id'))
)

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

    StreamBookMark = db.relationship('Stream', secondary=StreamBookMark,
                                        backref=db.backref('bookmarks', lazy='dynamic'))

    BranchBookMark = db.relationship('Branch', secondary=BranchBookMark,
                                        backref=db.backref('bookmarks', lazy='dynamic'))

    StreamThumbsUp = db.relationship('Stream', secondary=StreamThumbsUp,
                                        backref=db.backref('thumbsUps', lazy='dynamic'))

    BranchThumbsUp = db.relationship('Branch', secondary=BranchThumbsUp,
                                        backref=db.backref('thumbsUps', lazy='dynamic'))

    CommentThumbsUp = db.relationship('Comment', secondary=CommentThumbsUp,
                                        backref=db.backref('thumbsUps', lazy='dynamic'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.userName)

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

    StreamTagRelation = db.relationship('Tag', secondary=StreamTagRelation,
                                        backref=db.backref('streams', lazy='dynamic'))

    StreamBookMark = db.relationship('User', secondary=StreamBookMark,
                                        backref=db.backref('streamBookmarks', lazy='dynamic'))

    StreamThumbsUp = db.relationship('User', secondary=StreamThumbsUp,
                                        backref=db.backref('streamThumbsUps', lazy='dynamic'))

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

    #rootCardId = db.Column(db.Integer, db.ForeignKey('card.id'))
    rootCard = db.relationship('Card',
                           backref=db.backref('childBranches'))
    # card = db.relationship('Card',
    #                        backref=db.backref('childBranches', cascade='all, delete-orphan', lazy='dynamic'))

    # 현재 branch 객체가 참조하는 것이
    # stream 일땐 stream 에만 값 할당,
    # branch 일떈 branch 에만 값 할당

    parentBranchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
    parentBranch = db.relation('Branch', remote_side=[id])
    # childeBranch = db.relationship("Branch", lazy="joined", join_depth=2)
    # parentBranch = db.relationship('Branch',
    #                                backref=db.backref('childBranches', cascade='all, delete-orphan', lazy='dynamic',))

    parentStreamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
    stream = db.relationship('Stream',
                             backref=db.backref('childBranches', cascade='all, delete-orphan', lazy='dynamic'))

    BranchTagRelation = db.relationship('Tag', secondary=BranchTagRelation,
                                        backref=db.backref('branches', lazy='dynamic'))

    BranchBookMark = db.relationship('User', secondary=BranchBookMark,
                                        backref=db.backref('branchBookmarks', lazy='dynamic'))

    BranchThumbsUp = db.relationship('User', secondary=BranchThumbsUp,
                                        backref=db.backref('branchThumbsUps', lazy='dynamic'))


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
    __tablename__='StreamTitleKeyword'
    id = db.Column(db.Integer, primary_key=True)
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
    stream = db.relationship('Stream',
                             backref=db.backref('titleKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))

class StreamContentKeyword(db.Model):
    __tablename__='StreamContentKeyword'
    id = db.Column(db.Integer, primary_key=True)
    streamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
    stream = db.relationship('Stream',
                             backref=db.backref('contentKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))


class BranchTitleKeyword(db.Model):
    __tablename__='BranchTitleKeyword'
    id = db.Column(db.Integer, primary_key=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
    branch = db.relationship('Branch',
                             backref=db.backref('titleKeywords', cascade='all, delete-orphan', lazy='dynamic'))

    keyword = db.Column(db.String(50))


class BranchContentKeyword(db.Model):
    __tablename__='BranchContentKeyword'
    id = db.Column(db.Integer, primary_key=True)
    branchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
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

# class StreamTagRelation(db.Model):
#     __tablename__='StreamTagRelation'
#     id = db.Column(db.Integer, primary_key=True)
#     streamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
#     stream = db.relationship('Stream', backref=db.backref('tagRelations', cascade='all, delete-orphan', lazy='dynamic'))
#
#     tagId = db.Column(db.String(50), db.ForeignKey('tag.id'))
#     tag = db.relationship('Tag', backref=db.backref('streamRelations', cascade='all, delete-orphan', lazy='dynamic'))

# class BranchTagRelation(db.Model):
#     __tablename__='BranchTagRelation'
#     id = db.Column(db.Integer, primary_key=True)
#     branchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
#     branch = db.relationship('Branch', backref=db.backref('tagRelations', cascade='all, delete-orphan', lazy='dynamic'))
#
#     tagId = db.Column(db.String(50), db.ForeignKey('tag.id'))
#     tag = db.relationship('Tag', backref=db.backref('branchRelations', cascade='all, delete-orphan', lazy='dynamic'))

# class StreamBookMark(db.Model):
#     # __tablename__='StreamBookMark'
#     # id = db.Column(db.Integer, primary_key=True)
#     streamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
#     stream = db.relationship('Stream', backref=db.backref('bookmarks', cascade='all, delete-orphan', lazy='dynamic'))
#
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref=db.backref('streamBookmarks', cascade='all, delete-orphan', lazy='dynamic'))
#
#     cardId = db.Column(db.Integer, db.ForeignKey('card.id'))
#     card = db.relationship('Card', backref=db.backref('streamBookmarks', cascade='all, delete-orphan', lazy='dynamic'))
#
#     createDateTime = db.Column(db.DateTime, default=db.func.now())

# class BranchBookMark(db.Model):
#     __tablename__='BranchBookMark'
#     id = db.Column(db.Integer, primary_key=True)
#     branchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
#     branch = db.relationship('Branch', backref=db.backref('bookmarks', cascade='all, delete-orphan', lazy='dynamic'))
#
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref=db.backref('branchBookmarks', cascade='all, delete-orphan', lazy='dynamic'))
#
#     cardId = db.Column(db.Integer, db.ForeignKey('card.id'))
#     card = db.relationship('Card', backref=db.backref('branchBookmarks', cascade='all, delete-orphan', lazy='dynamic'))
#
#     createDateTime = db.Column(db.DateTime, default=db.func.now())

# class StreamThumbsUp(db.Model):
#     __tablename__='StreamThumbsUp'
#     id = db.Column(db.Integer, primary_key=True)
#     streamId = db.Column(db.Integer, db.ForeignKey('stream.id'))
#     stream = db.relationship('Stream', backref=db.backref('thumbsUps', cascade='all, delete-orphan', lazy='dynamic'))
#
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref=db.backref('streamThumbsUps', cascade='all, delete-orphan', lazy='dynamic'))
#
#     createDateTime = db.Column(db.DateTime, default=db.func.now())

# class BranchThumbsUp(db.Model):
#     __tablename__='BranchThumbsUp'
#     id = db.Column(db.Integer, primary_key=True)
#     branchId = db.Column(db.Integer, db.ForeignKey('branch.id'))
#     branch = db.relationship('Branch', backref=db.backref('thumbsUps', cascade='all, delete-orphan', lazy='dynamic'))
#
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref=db.backref('branchThumbsUps', cascade='all, delete-orphan', lazy='dynamic'))
#
#     createDateTime = db.Column(db.DateTime, default=db.func.now())

# class CommentThumbsUp(db.Model):
#     __tablename__='CommentThumbsUp'
#     id = db.Column(db.Integer, primary_key=True)
#     commentId = db.Column(db.Integer, db.ForeignKey('comment.id'))
#     comment = db.relationship('Comment', backref=db.backref('thumbsUps', cascade='all, delete-orphan', lazy='dynamic'))
#
#     userId = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', backref=db.backref('commentThumbsUps', cascade='all, delete-orphan', lazy='dynamic'))
#
#     createDateTime = db.Column(db.DateTime, default=db.func.now())

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
