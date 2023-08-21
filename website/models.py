from . import db #bc already in the website folder
from flask_login import UserMixin

#create the tables to store our data

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category_id = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#getting it from the key in user class - it's lowercase

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    firstname = db.Column(db.String)
    transaction = db.relationship('Transaction')#for relationship it has to be actual reference to class (keep the uppercase)

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True, nullable=False)
#     transactions = db.relationship('Transaction')
