from flask import Flask,request,jsonify
from application.database import db
from flask_restful import Api
from flask_cors import CORS
from application.config import Config
from application.models import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash,check_password_hash
from application.api import *
from application.tasks import cel_app


app = None
api = None
user_datastore = None

def create_app():
    #flask instance
    app = Flask(__name__)
    app.config.from_object(Config)

    #database
    db.init_app(app)

    #api instance
    api = Api(app)

    #jwt
    jwt = JWTManager(app)

    #cors
    CORS(app)

    #celery
    celery = cel_app

    celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    enable_utc=app.config["ENABLE_UTC"],
    timezone=app.config["TIMEZONE"],
)
    class FlaskTask(celery.Task):
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return self.run(*args,**kwargs)
            
    celery.Task=FlaskTask

    return app,api,celery

def initialize():
    with app.app_context():
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()

        if not table_names: 
            # If no tables exist
            db.create_all()

            #creating roles
            super_admin_role = Role(name='super admin',description="Super Administrator")
            admin_role = Role(name='admin',description="Support staff")
            student_role = Role(name="student",description="Student")

            db.session.add_all([super_admin_role,admin_role,student_role])
            db.session.commit()
            
            #creating super_admin
            super_admin_user=User(
                name="SuperAdmin",email='xyz@superadmin.mail.com',
                username="superadmin",
                password=generate_password_hash('password'),
                level="Super Admin",role="super admin"
                )
            db.session.add(super_admin_user)
            db.session.commit()

            print("Database tables created.")
        else:
            print("Database tables already exist.")

app,api,celery= create_app()
initialize()


#add resources
api.add_resource(StudentRegisterAPI,"/api/student_signup")
api.add_resource(AdminRegisterAPI,"/api/admin_signup")
api.add_resource(LoginAPI,"/api/login")
api.add_resource(VerifyToken,"/api/verify_token")
api.add_resource(InterviewAPI,"/api/interview","/api/interview/<int:id>")
api.add_resource(QuestionAPI,"/api/question","/api/question/<int:id>")
api.add_resource(PracticeTestAPI,"/api/practice_tests","/api/practice_tests/<int:id>")
api.add_resource(UsersAPI,"/api/users","/api/users/<int:id>")
api.add_resource(PostsAPI,"/api/posts","/api/posts/<int:postid>")
api.add_resource(RepliesAPI,"/api/reply","/api/reply/<int:replyid>")
api.add_resource(Forgot_Password,"/forgot_password")
api.add_resource(Verify_Pin,"/verify_pin")
api.add_resource(Reset_Password,"/reset_password")


if __name__=="__main__":
    app.run(debug=True,
            port=3000)