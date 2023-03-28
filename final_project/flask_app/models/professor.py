from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



class Professor:
    db="university"
    def __init__(self,data):
        self.id  = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO professors (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM professors WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM professors WHERE email = %(email)s;"
        results = connectToMySQL(Professor.db).query_db(query,user)
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM professors WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])