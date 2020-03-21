from app import db
import time


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    course = db.Column(db.Integer)
    student_number = db.Column(db.Integer)

    def __init__(self, fname, lname, email, course, student_number):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.course = course
        self.student_number = student_number