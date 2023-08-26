from application.database import db
from datetime import datetime
from utils.custom_column import Json, List


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    level = db.Column(db.String,nullable=False)
    github_link = db.Column(db.String,unique=True)
    linkedin_link = db.Column(db.String,unique=True)
    active = db.Column(db.Boolean(),default=True)
    forgot_password_pin=db.Column(db.String,nullable=True)
    pin_generated_time = db.Column(db.DateTime,nullable=True)
    
    #one to one with roles table
    role = db.Column(db.String,db.ForeignKey('role.name'))
    #one to many with posts table
    posts = db.relationship("Posts",backref="posted_by")
    #one to many with interviews table
    interviews = db.relationship("Interviews",backref="created_by")
    #one to many with Replies table
    replies = db.relationship("Replies",backref="replied_by")
    
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))



class Posts(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String,nullable=False)
    tags = db.Column(List,nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.today(),nullable=False)
    
    #foreignkey with User table
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    #one to many relation with replies table
    replies = db.relationship("Replies",backref="post",cascade="all,delete-orphan")

class Replies(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String,nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.today(),nullable=False)
    
    #foreignkeys with User and Posts table
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))

class Interviews(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company = db.Column(db.String,nullable=False)
    job_role = db.Column(db.String,nullable=False)
    job_type = db.Column(db.String,nullable=False)
    anonymous = db.Column(db.Boolean(),default=False)
    description = db.Column(db.String,nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.today(),nullable=False)
    
    #foreignkey
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)


#secondary table between Qeustions and PracticeTests
ques_practice = db.Table('ques_practice',
        db.Column('ques_Id', db.Integer(), db.ForeignKey('questions.id')),
        db.Column('test_id', db.Integer(), db.ForeignKey('practicetests.id')))

class Questions(db.Model):
    __tablename__="questions"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tags = db.Column(List,nullable=False) 
    description = db.Column(db.String,nullable=False)
    question_type = db.Column(db.String,nullable=False) # one of MCQ, MSQ, NAT, Coding
    options = db.Column(Json, default=None) # Custom column type
    correct_answers = db.Column(List)

class PracticeTests(db.Model):
    __tablename__="practicetests"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tags = db.Column(List,nullable=False)
    
    # many to many relation with Questions table
    questions = db.relationship("Questions",secondary=ques_practice,backref=db.backref('tests', lazy='dynamic'))

