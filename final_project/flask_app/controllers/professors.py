from flask import render_template, redirect, session, request, flash, url_for
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.professor import Professor
from flask_app.models.course import Course
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    if not Professor.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Professor.save(data)
    session['professors_id'] = id

    return redirect('/home')

@app.route("/home")
def home():

    if'professors_id' not in session:
        return redirect('/logout')
    data = {
        'id' :session['professors_id']
    }
    return render_template("home.html", professor= Professor.get_by_id(data), courses= Course.show_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    professor = Professor.get_by_email(request.form)

    if not professor:
        flash("Invalid Email,","login")
        return redirect('/')
    if not bcrypt.check_password_hash(professor.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['professors_id'] = professor.id
    return redirect('/home')

@app.route("/catalog")
def catalog():
    if'professors_id' not in session:
        return redirect('/logout')
    data = {
        'id' :session['professors_id']
    }
    return render_template("catalog.html", professor_one= Professor.get_by_id(data), all_courses= Course.show_all())

@app.route("/contact")
def contact():
    return render_template("contact.html")
