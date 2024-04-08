from flask import Flask,render_template,redirect,request,session,flash,url_for
from flask_app import app
from flask_app.models.tasks import task
from flask_app.models.users import User

@app.route('/show_task')
def show_task():
    if 'user_id' in session:
        frm_id={'id':session['user_id']}
        obj_tasks=task.get_task_user(frm_id)
        obj_task_past= task.get_task_user_past(frm_id)
        user= User.get_by_id(frm_id)
        return render_template('dashboard.html',user=user,tasks=obj_tasks,tasks_past=obj_task_past)
    return redirect('/')

@app.route('/crear_task',methods=['post'])
def create_task():
    if 'user_id' in session:
        if task.validate_new_task(request.form):
            task.save_task(request.form)
            return redirect('/show_task')
        else:
            return render_template('new_task.html')
    return redirect('/')

@app.route('/delete_task/<int:id_task>', methods=['POST'])
def delete_task(id_task):
    if 'user_id' in session:
        frm= {'id':id_task}
        task_obj= task.get_task_by_id(frm)
        if task.validate_edit_delete_task(task_obj[0]):
            frm_id_task={'id':id_task}
            task.delete_task(frm_id_task)
            return redirect('/show_task')
        else:
            return redirect('/show_task')
    return redirect('/')

@app.route('/edit_task/<int:id_task>', methods=['POST'])
def edittask(id_task):
    if 'user_id' in session:
        frm= {'id':id_task}
        task_obj= task.get_task_by_id(frm)
        if task.validate_edit_delete_task(task_obj[0]):
            frm_id_task={'id':id_task}
            task_n=task.get_task_by_id(frm_id_task)
            return render_template('edittask.html', task=task_n[0])
        else:
            return redirect('/show_task')
    return redirect('/')

@app.route('/edit_tasks', methods=['POST'])
def edit_task():
    if 'user_id' in session:
        # Copiar datos de request.form a un diccionario estándar para manipulación
        form_data = {'task': request.form['task'],
                    'date_task': request.form['date_task'],
                    'action': request.form['action'],
                    'id': request.form.get('task_id', None)}
        if task.validate_new_task(form_data):
            task.edit_task(form_data)
            return redirect('/show_task')
        else:
            frm_id_task={'id':form_data['id']}
            task_n=task.get_task_by_id(frm_id_task)
            return render_template('edittask.html', task=task_n[0])
    return redirect('/')



