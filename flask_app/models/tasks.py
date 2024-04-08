from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import pytz
from datetime import datetime

class task():
    def __init__(self,data):
        self.id =data['id']
        self.task= data['task']
        self.action= data['action']
        self.date_task=data['date_task']
        self.created_at= data['created_at']
        self.updated_at = data['updated_at'] 
        self.user_id= data['user_id']

    @classmethod 
    def save_task(cls,frm):
        #this frm was send for the web user
        query= 'INSERT INTO appointments(task,action,date_task,user_id) VALUES(%(task)s,%(action)s,%(date_task)s,%(user_id)s)'
        result= connectToMySQL('app_user').query_db(query,frm)
        return result    
    
    @classmethod
    def get_task_user(cls,frm):
        query= 'SELECT ap.* FROM appointments as ap INNER JOIN user ON user.id= ap.user_id WHERE user.id= %(id)s ORDER BY ap.date_task DESC'
        resp= connectToMySQL('app_user').query_db(query,frm)
        task_lst=[]
        if len(resp)>0:
            for obj in resp:
                task_lst.append(cls(obj))
        return task_lst
    
    @classmethod
    def get_task_user_past(cls,frm):
        query= 'SELECT ap.* FROM appointments as ap INNER JOIN user ON user.id= ap.user_id WHERE user.id= %(id)s  AND ap.date_task < NOW() ORDER BY ap.date_task DESC'
        resp= connectToMySQL('app_user').query_db(query,frm)
        task_lst=[]
        if len(resp)>0:
            for obj in resp:
                task_lst.append(cls(obj))
        return task_lst
    
    @classmethod
    def delete_task(cls,frm):
        query= 'DELETE FROM appointments WHERE appointments.id= %(id)s'
        resp= connectToMySQL('app_user').query_db(query,frm)
        return resp
    
    @classmethod
    def get_task_by_id(cls,frm):
        query= 'SELECT * FROM appointments WHERE appointments.id= %(id)s'
        resp= connectToMySQL('app_user').query_db(query,frm)
        print(resp)
        task_lst=[]
        if len(resp)>0:
            for obj in resp:
                task_lst.append(cls(obj))
        return task_lst
    
    @classmethod 
    def edit_task(cls,frm):
        query= 'UPDATE appointments SET task= %(task)s, action= %(action)s , date_task=%(date_task)s WHERE id= %(id)s'
        result= connectToMySQL('app_user').query_db(query,frm)
        print(result)
        return result 
    
    @staticmethod
    def validate_new_task(frm):
        is_valid=True
        if len(frm['task'])<3:
            flash('The task should be at less 3 characters','task_register')
            is_valid=False
        if  frm['date_task'] =='':
            flash('The task date should be in the future','task_register')
            is_valid=False
        else:         
            date_task = datetime.strptime(frm['date_task'] , '%Y-%m-%d') 
            now = datetime.now()   
            if date_task < now:
                flash('The task date should be in the future','task_register')
                is_valid=False  
        if 'action' not in frm:
            flash('The action should have a value','task_register')
            is_valid=False      
        return is_valid 
    @staticmethod
    def validate_edit_delete_task(obj):
        is_valid=True
        if obj.action =='Done':
            is_valid=False
            flash('The task does not posible to edit or delete','task_delete')
        return is_valid    




