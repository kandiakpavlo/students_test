import json

from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView

from .database import db
from .models import Users


class JustToJson(dict):
    def __str__(self):
        return json.dumps(self)


students_api = Blueprint('students_api', __name__)


class StudentsApi(MethodView):
    """ /students"""

    good = {
        "delete": {
            "status": "OK", "message": "We delete your users"
        },
        "add": {
            "status": "OK",
            "message": "We add your user"
        }
    }

    error = {
        "itemAlreadyExists": {
            "errorCode": "itemAlreadyExists",
            "errorMessage": "Could not create item. Item already exists"
        }
    }

    def post(self):
        """ Add a student"""
        params = json.loads(request.data.decode('utf-8'))
        student_number = [*params.keys()][0]
        user = Users.query.filter_by(student_number=student_number).first()
        if user:
            return make_response(jsonify(self.error["itemAlreadyExists"]), 400)
        user = Users(
            fname=params[f'{student_number}']['first_name'],
            lname=params[f'{student_number}']['last_name'],
            email=params[f'{student_number}']['email'],
            course=params[f'{student_number}']['course'],
            student_number=student_number
        )
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify(self.good["add"]), 200)

    def get(self):
        my_query = Users.query.all()
        users_list = []
        for user in my_query:
            users = [f"{user.student_number}", {
                "first_name": user.fname,
                "last_name": user.lname,
                "email": user.email,
                "course": user.course}
                     ]
            users_list.append(users)
        users = JustToJson(users_list)
        return make_response(jsonify(users), 200)

    def delete(self):
        Users.query.delete()
        db.session.commit()
        return make_response(jsonify(self.good["delete"]), 200)


class StudentsIdApi(MethodView):
    """ /students/<student_number> """

    error = {
        "itemNotFound": {
            "errorCode": "itemNotFound",
            "errorMessage": "Item not found"
        },
        "itemAlreadyExists": {
            "errorCode": "itemAlreadyExists",
            "errorMessage": "Could not create item. Item already exists"
        }
    }

    good = {
        "add": {
            "status": "OK",
            "message": "We add your user"
        },
        "delete": {
            "status": "OK",
            "message": "We delete your user"
        },
        "apdate": {
            "status": "OK",
            "message": "We apdate your user"
        }
    }

    def get(self, student_number):
        """ Get a student"""
        user = Users.query.filter_by(student_number=student_number).first()
        if not user:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        user_json = {
            f"{user.student_number}": {
                "first_name": user.fname,
                "last_name": user.lname,
                "email": user.email,
                "course": user.course}
        }
        return make_response(jsonify(user_json), 200)

    def put(self, student_number):
        """ Update/replace an item """
        params = json.loads(request.data.decode('utf-8'))
        user = Users.query.filter_by(student_number=student_number).first()
        if not user:
            user = Users(
                fname=params['fname'],
                lname=params['lname'],
                email=params['email'],
                course=params['course'],
                student_number=student_number
            )
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(self.good["add"]), 200)
        user.fname = params['fname']
        user.lname = params['lname']
        user.email = params['email']
        user.course = params['course']
        db.session.commit()
        return make_response(jsonify(self.good["apdate"]), 200)

    def patch(self, student_number):
        """ Update student's course """
        params = json.loads(request.data.decode('utf-8'))
        user = Users.query.filter_by(student_number=student_number).first()
        if not user:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        user.course = params['course']
        db.session.commit()
        return make_response(jsonify(self.good["apdate"]), 200)

    def delete(self, student_number):
        """ Delete a student """
        user = Users.query.filter_by(student_number=student_number).first()
        if not user:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        Users.query.filter_by(student_number=student_number).delete()
        db.session.commit()
        return make_response(jsonify(self.good["delete"]), 200)


students_api.add_url_rule("/students", view_func=StudentsApi.as_view("students_api"))
students_api.add_url_rule("/students/<student_number>", view_func=StudentsIdApi.as_view("students_id_api"))
