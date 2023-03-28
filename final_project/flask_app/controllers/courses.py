from flask import render_template, redirect,session, request, flash
from flask_app import app
from flask_app.models.professor import Professor
from flask_app.models.course import Course

@app.route("/post", methods = ['POST'])
def create_course():
    print(request.form)
    Course.save(request.form)
    return redirect("/home")

@app.route("/new/course")
def new_course():
    if "professors_id" not in session:
        return redirect('/logout')
    data = {
        "id": session['professors_id']
    }

    return render_template("add_course.html", professor=Professor.get_by_id(data))

@app.route('/course/<int:id>')
def show_course(id):
    print('course')
    if 'professors_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    professor_data = {
        "id":session['professors_id']
    }
    return render_template("show.html",course=Course.get_one(data),professor=Professor.get_by_id(professor_data))

@app.route('/edit/course/<int:id>')
def edit(id):
    if 'professors_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    professor_data = {
        "id":session['professors_id']
    }
    return render_template("edit.html",edit=Course.get_one(data),professor=Professor.get_by_id(professor_data))

@app.route('/update/show',methods=['POST'])
def update():
    print(11)
    if 'professors_id' not in session:
        return redirect('/logout')
    if not Course.validate_course(request.form):
        return redirect('/new/show')
    data = {
        "name" : request.form["name"],
        "quarter" : request.form["quarter"],
        "building" : request.form["building"],
        "ta" : request.form["ta"],
        "id" : request.form['id']
    }
    print(1, data)
    Course.update(data)
    return redirect('/home')

@app.route("/delete/course/<int:id>")
def delete_post(id):
    if 'professors_id' not in session:
        return redirect('/home')
    data = {
        "id":id
    }
    Course.delete(data)
    return redirect('/home')