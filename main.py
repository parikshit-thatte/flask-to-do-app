from flask import Flask, request, flash, url_for, redirect, render_template, session
from markupsafe import escape
from db import *


@app.route("/")
def landing_page():
    return render_template("index.html")


@app.route("/register")
def register_user():
    return render_template("registerUser.html")


@app.route("/addNewUser", methods=['GET', 'POST'])
def add_new_user():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pwd']
        password2 = request.form['pwd2']

        if(password == password2):
            new_user = User(username=escape(username), password=escape(password))
            db.session.add(new_user)
            db.session.commit()
            flash('You were successfully Registered!')
            return redirect(url_for('landing_page'))

    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=escape(request.form['username'])).first()

        if user.password == request.form['pwd']:
            session['username'] = user.username
            return redirect(url_for('todolist'))
        else:
            flash('Username or password was incorrect!') 
            return redirect(url_for('landing_page'))


@app.route("/todolist")
def todolist():
    if 'username' in session:
        user = User.query.filter_by(username=escape(session['username'])).first()
        todo_items = ToDoList.query.filter_by(created_by=user.id)

        if todo_items:
            return render_template("ToDoApp.html", todo_items=todo_items)
        else:
            return render_template("ToDoApp.html", todo_items=None)
    
    flash('Please login to access this page...')
    return redirect(url_for('landing_page'))


@app.route("/addTodoTask")
def addTodoTask():
    if 'username' in session:
        return render_template("addTodoTask.html")


@app.route("/addNewTask", methods=['GET', 'POST'])
def addNewTask():
    if 'username' in session:
        error = None
        if request.method == 'POST':
            user = User.query.filter_by(username=escape(session['username'])).first()
            new_task = ToDoList(name = escape(request.form['taskname']), created_by = user.id)
            db.session.add(new_task)
            db.session.commit()

            flash('Task added successfully!')

            return redirect(url_for('todolist'))


@app.route('/deleteTask/<int:task_id>')
def delete_task(task_id):
    if 'username' in session:
        item = ToDoList.query.filter_by(id=task_id).first()
        db.session.delete(item)
        db.session.commit()

        flash('Task deleted successfully!')
        return redirect(url_for('todolist'))


@app.route("/updateTask/<int:task_id>")
def updateTaskPage(task_id):
    if 'username' in session:
        item = ToDoList.query.filter_by(id=task_id).first()
        return render_template("updateTask.html",  item=item)


@app.route('/updateTaskToDB/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if 'username' in session:
        if request.method == 'POST':
            item = ToDoList.query.filter_by(id=task_id).first()
            setattr(item, 'task_name', request.form['taskname'])
            db.session.commit()

            flash('Task updated successfully!')
            return redirect(url_for('todolist'))


@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)

        return redirect(url_for('landing_page'))