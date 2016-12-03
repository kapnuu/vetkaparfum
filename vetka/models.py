from vetka import db
from enum import Enum


class Priority(Enum):
    low = 1
    normal = 2
    high = 3


GoodTag = db.Table('good_tag',
                   db.Column('good_id', db.Integer, db.ForeignKey('good.id')),
                   db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Good(db.Model):
    __tablename__ = 'good'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    image = db.Column(db.String)
    name_en = db.Column(db.String)
    price = db.Column(db.Integer)
    priority = db.Column(db.Integer, default=2)
    deleted = db.Column(db.Boolean, default=False)
    tags = db.relationship('Category',
                           secondary=GoodTag,
                           lazy='dynamic')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    name_en = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=0)
    goods = db.relationship('Good', backref='category', lazy='dynamic')
    goods2 = db.relationship('Good', secondary=GoodTag, lazy='dynamic')
    primary = db.Column(db.Boolean, default=0)


