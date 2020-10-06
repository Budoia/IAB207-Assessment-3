from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column (db.String(100), index=True, unnique=True, nullable=False)
    emailid = db.Column(db.String(100), index-True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    #Relationship
    comments = db.relationship('Comment', backref='user')

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(400))
    currency = db.Column(db.String(4), nullable=False)

    #Relationship
    comments = db.relationship('Comment', backref='destination')

    def __repr__(self):
        return ",Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    #Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    def __repr__(self):
        return ",Comment: {}>".format(self.text)

# class Destination:

#     def __init__(self, name, description, image_url, currency):
#         self.name = name
#         self.description = description
#         self.image = image_url
#         self.currency = currency
#         self.comments = list()

#     def set_comments(self,comment):
#         self.comments.append(comment)

#     def __repr__(self):
#         str = 'Name {0} , Currency {1}'
#         str.format(self.name, self.currency)
#         return str


# class Comment:
#     def __init__(self,user, text, created_at):
#         self.user = user
#         self.text = text
#         self.create_at = created_at

#     def __repr__(self):
#         str = 'User {0}, \n Text {1}'
#         str.format(self.user, self.text)
#         return str