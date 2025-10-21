# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class User(db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)

    #__User_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    username = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    role = db.Column(db.Text, nullable=True)

    #__User_FIELDS__END

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Note(db.Model):

    __tablename__ = 'Note'

    id = db.Column(db.Integer, primary_key=True)

    #__Note_FIELDS__
    id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.Text, nullable=True)
    uploader_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Note_FIELDS__END

    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)


class Category(db.Model):

    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)

    #__Category_FIELDS__
    name = db.Column(db.Text, nullable=True)
    descreption = db.Column(db.Text, nullable=True)

    #__Category_FIELDS__END

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)



#__MODELS__END
