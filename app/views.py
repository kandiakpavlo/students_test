from flask import Blueprint, render_template, request, flash, redirect, url_for
from .database import db
from .models import users, articles


st = Blueprint('students', __name__, template_folder='template', url_prefix='/students/')
bp = Blueprint('other', __name__, template_folder='template')


@bp.route('/')
def home():
    return render_template("home.html", article=articles.query.all()[::-1])


@bp.route('/add_article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        article = request.form['article']
        art = articles(title, article)
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('other.add_article'))
    return render_template('articles.html')


@st.route('/<usr>')
def user(usr):
    return render_template("index.html", usr=usr)


@st.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        course = request.form['course']
        user = users(fname, lname, email, course)
        db.session.add(user)
        db.session.commit()
        return render_template('index.html', usr=user)
    else:
        return render_template('add.html', title='Add student')


@st.route('/all', methods=['GET', 'POST'])
def all():
    if request.method == "POST":
        id = request.form['id']
        users.query.filter_by(_id=id).delete()
        db.session.commit()
        return render_template('all.html', all=users.query.all())
    return render_template('all.html', all=users.query.all())


@st.route('/course/<course>')
def other_course(course):
    return render_template('all.html', all=users.query.filter_by(course=course))