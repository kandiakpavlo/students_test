from app import db
import time


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    course = db.Column(db.Integer)

    def __init__(self, fname, lname, email, course):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.course = course


class articles(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    article = db.Column(db.String(100))
    date = db.Column(db.String(50))

    def __init__(self, title, article):
        self.title = title
        self.article = article
        self.date = time.strftime("%d %B %Y %H:%M:%S")