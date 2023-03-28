from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.professor import Professor

class Course:
    db="university"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.quarter = data['quarter']
        self.building = data['building']
        self.ta = data['ta']
        self.professors_id = data['professors_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        if not cls.validate_course(data):
            print("in save if not valid...")
            return False
        print("Data passed into create METHOD: ",data)

        query = "INSERT INTO courses (name, quarter, building, ta, professors_id) VALUES (%(name)s, %(quarter)s, %(building)s, %(ta)s, %(professors_id)s);"
        result = connectToMySQL(cls.db).query_db(query,data)

        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM courses WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def show_all(cls):
        query = "SELECT * FROM courses;"
        results =  connectToMySQL(cls.db).query_db(query)
        all_courses = []
        for row in results:
            all_courses.append( cls(row) )
        return all_courses

    @staticmethod
    def validate_course(course):
        is_valid = True
        if len(course['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","course")
        if len(course['quarter']) < 3:
            is_valid = False
            flash("Quarter must be at least 3 characters","course")
        if len(course['building']) < 3:
            is_valid = False
            flash("building must be at least 3 characters","course")
        if len(course['ta']) < 3:
            is_valid = False
            flash("ta must be at least 3 characters","course")
        return is_valid
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM courses WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0]) 
    
    @classmethod
    def update(cls, data):
        print(data)
        query = """
                UPDATE courses
                SET name = %(name)s, quarter = %(quarter)s, building = %(building)s, ta = %(ta)s
                WHERE id = %(id)s;
                """

        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM courses WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)