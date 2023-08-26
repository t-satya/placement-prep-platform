from flask import request
from flask_restful import Resource
from application.models import User
from utils.error_codes import AuthenticationAPIErrors
from werkzeug.security import generate_password_hash
from application.database import db
import random
from jinja2 import Template
from application.tasks import send_mail
from datetime import datetime,timedelta

class Forgot_Password(Resource):
    def post(self):
        """
            In the case of forgot_password the user can enter his/her
            username or email as input.
            {
                "user_input":"xyz@mail.com"
            }
            Returns:
                An email will be sent to the user with a random 6 digit code.
                
                dict: A dictionary containing the message indicating success or error, 
                    along with user's email that will be stored in localstorage
                    for the next fetch calls
        """
        try:
            data=request.json
            user_input = data.get("user_input")
            user_check = db.session.query(User).filter((User.username == user_input) | (User.email == user_input)).first()
            if not user_input:
                return {"msg":AuthenticationAPIErrors.COMPULSORY_EMAIL.description}, AuthenticationAPIErrors.COMPULSORY_EMAIL.status_code
            if not user_check:
                return {"msg":AuthenticationAPIErrors.USER_NOT_FOUND.description}, AuthenticationAPIErrors.USER_NOT_FOUND.status_code

            random_pin=str(random.randint(100000, 999999))
            user_check.forgot_password_pin=random_pin
            user_check.pin_generated_time=datetime.now()
            db.session.commit()
            with open("templates/forgot_password.html") as file_:
                template= Template(file_.read())
                message = template.render(pin=random_pin)
            send_mail.delay(user_check.email,subject="Pin to reset your password",message=message)
            return {"msg":"Success","email":user_check.email}
            
        except Exception as e:
            print(e)
            return {"msg" : AuthenticationAPIErrors.INTERNAL_ERROR.description } , AuthenticationAPIErrors.INTERNAL_ERROR.status_code

    
class Verify_Pin(Resource):
    def post(self):
        """
            In the case of verity_pin the user can enter his/her pin
            received on email
            The email address of the user is extracted from the localStorage and 
            added in the fetch call body
            {
                "email":"xyz@mail.com",
                "entered_pin":"123456"
            }
            Returns:
                
                dict: A dictionary containing the message indicating success or error, 
                    along with user's email that will be stored in localstorage
                    for the next fetch calls
        """
        try:
            data=request.json
            entered_pin=data.get("entered_pin")
            mail=data.get("email")
            current_time = datetime.now()
            check_user=User.query.filter_by(email=mail).first() 
            if not data.get("email"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_EMAIL.description } , AuthenticationAPIErrors.COMPULSORY_EMAIL.status_code 
            if not check_user:
                return {"msg":AuthenticationAPIErrors.USER_NOT_FOUND.description}, AuthenticationAPIErrors.USER_NOT_FOUND.status_code
            if current_time-check_user.pin_generated_time >= timedelta(minutes=10):
                return {"msg":AuthenticationAPIErrors.TOKEN_EXPIRED.description}, AuthenticationAPIErrors.TOKEN_EXPIRED.status_code
            if check_user.forgot_password_pin!=entered_pin:
                return {"msg":AuthenticationAPIErrors.INVALID_PIN.description}, AuthenticationAPIErrors.INVALID_PIN.status_code
            return {"msg":"Success","email":check_user.email}
        
        except Exception as e:
                print(e)
                return {"msg" : AuthenticationAPIErrors.INTERNAL_ERROR.description } , AuthenticationAPIErrors.INTERNAL_ERROR.status_code


class Reset_Password(Resource):
    def post(self):
        """
            In the case of verity_pin the user can enter his/her pin
            received on email
            The email address of the user is extracted from the localStorage and 
            added in the fetch call body
            {
                "email":"xyz@mail.com",
                "new_password":"123456"
                "confirm_password":"123456"
            }
            Returns:
                An email will be sent to the user on successful password update.
               
                dict: A dictionary containing the message indicating success or error, 
                    
        """
        try:
            data=request.json
            user_email = data.get("email")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if not data.get("email"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_EMAIL.description } , AuthenticationAPIErrors.COMPULSORY_EMAIL.status_code 
            if not new_password or not confirm_password:
                return {"msg":AuthenticationAPIErrors.COMPULSORY_PASSWORD.description}, AuthenticationAPIErrors.COMPULSORY_PASSWORD.status_code
            if new_password!=confirm_password:
                return {"msg":AuthenticationAPIErrors.PASSWORD_NOT_MATCH.description}, AuthenticationAPIErrors.PASSWORD_NOT_MATCH.status_code
            
            get_user = User.query.filter_by(email=user_email).first()
            get_user.password=generate_password_hash(new_password)
            db.session.commit()
            with open("templates/password_changed.html") as file_:
                template= Template(file_.read())
                message = template.render(user_name=get_user.username)
            send_mail.delay(get_user.email,subject="Password changed successfully",message=message)
            return {"msg":"Success"}
            
        except Exception as e:
            print(e)
            return {"msg":AuthenticationAPIErrors.INTERNAL_ERROR.description}, AuthenticationAPIErrors.INTERNAL_ERROR.status_code
