from flask import Flask,render_template,redirect,request,session,flash,url_for
from flask_app import app
from flask_app.models.users import User
from flask_app.models.tasks import task
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['post'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pass_encrypt= bcrypt.generate_password_hash(request.form['password'])
    form={'first_name': request.form['first_name'],'last_name': request.form['last_name'],'email': request.form['email'],
        'password': pass_encrypt}
    id_user=User.save(form)
    session['user_id']=id_user# This register is use it to validate in a dashboard for example...
    return redirect('/dashboard')    

@app.route('/dashboard')
def dashboard():
    #Verify user before access to dashboard
    if 'user_id' in session:
        #Create an instance user in based sessions
        frm={'id':session['user_id']}
        user= User.get_by_id(frm)
        obj_tasks=task.get_task_user(frm)
        obj_task_past= task.get_task_user_past(frm)
        return render_template('dashboard.html',user=user,tasks=obj_tasks,tasks_past=obj_task_past)
    return redirect('/')

@app.route('/login', methods=['post'])
def login():
    #verify email existe
    user= User.get_by_email(request.form)
    if not user:
        flash('E-mail does not exist','login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Incorrect password','login')
        return redirect('/')
    else:
        session['user_id']=user.id
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/new_task')
def new_task():
    if 'user_id' in session:
        #Create an instance user in based sessions
        frm={'id':session['user_id']}
        user= User.get_by_id(frm)
        return render_template('new_task.html')
    return redirect('/')

