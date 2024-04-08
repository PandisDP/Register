from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class User:
    def __init__(self,data):
        self.id= data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email= data['email']
        self.password = data['password']
        self.created_at= data['created_at']
        self.updated_at = data['updated_at'] 
    @classmethod
    def save(cls,frm):
        #this frm was send for the web user
        query= 'INSERT INTO user(first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)'
        result= connectToMySQL('app_user').query_db(query,frm)
        return result
    @staticmethod
    def validate_user(frm):
        is_valid=True
        if len(frm['first_name'])<3:
            flash('First Name should be at less 3 characters','register')
            is_valid=False
        if  len(frm['last_name'])<3:    
            flash('Last Name should have at less 3 characters','register')
            is_valid=False
        if not EMAIL_REGEX.match(frm['email']):
            flash('The email format is not valid','register')
            is_valid=False
        if  len(frm['password'])<8:    
            flash('Password should have at less 8 characters','register')
            is_valid=False 
        if not re.search("[0-9]", frm['password']):
            flash('Password should have at least one number', 'register')
            is_valid = False
        if not re.search("[A-Z]", frm['password']):
            flash('Password should have at least one uppercase letter', 'register')
            is_valid = False    
        # Validate the existence of email    
        query= 'SELECT * FROM user WHERE email=%(email)s' 
        resp= connectToMySQL('app_user').query_db(query,frm) 
        if len(resp)>0:
            flash('The email exist!!!','register')
            is_valid=False  
        # Password Confirm
        if frm['password']!=frm['confirm']:
            flash('The password not math with confirm','register')
            is_valid=False                  
        return is_valid
    
    @classmethod
    def get_by_email(cls,frm):
        query= 'SELECT * FROM user WHERE email=%(email)s' 
        resp= connectToMySQL('app_user').query_db(query,frm)
        if len(resp)==1:
            user= cls(resp[0])
            return user
        else:
            return False
    @classmethod
    def get_by_id(cls,frm):
        query= 'SELECT * FROM user WHERE id= %(id)s'
        resp= connectToMySQL('app_user').query_db(query,frm)
        if len(resp)==1:
            user= cls(resp[0])
            return user
        else:
            return False






    