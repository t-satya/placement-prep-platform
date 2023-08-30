from flask import jsonify,request,abort
import re
from flask_restful import Resource
from application.models import User
from application.database import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,create_access_token, get_jwt_identity
from utils.roles_accepted import roles_accepted
from utils.error_codes import AuthenticationAPIErrors
from utils.constants import USER_LEVELS_ALLOWED, ADMIN_LEVELS_ALLOWED
from application.tasks import send_mail
from jinja2 import Template

username_pattern = re.compile(r'^[a-zA-Z0-9_]{3,20}$')

class StudentRegisterAPI(Resource):
    """
    API endpoint for registering new students.

    This class handles HTTP POST requests to register new students.

    Methods:
        post(): Handles the HTTP POST request for registering a new student.

    Required Data in JSON Payload:
        The HTTP POST request to this endpoint must include the following data
        in JSON format:\n
        {
            "email": "student_email@example.com",                           # Student's email (string)\n
            "password": "password123",                                      # Student's password (string)\n
            "confirm_password": "password123",                              # Student's password for confirmation(string)\n
            "name": "John Doe",                                             # Student's full name (string)\n
            "username" : "JohnDoe"
            "level": "BSc",                                                 # Student's education level (string)\n
            "github_link": "https://github.com/johndoe",                    # Link to student's GitHub profile (string)\n
            "linkedin_link": "https://www.linkedin.com/in/johndoe"          # Link to student's LinkedIn profile (string)\n
        }\n

    Example Usage:
        To register a new student, make an HTTP POST request to the API endpoint
        provided by this class with the required student information in JSON format.
    """

    # def delete(self):
    #     user = User.query.filter_by(email="ritikkaushallvb@gmail.com").first()

    #     db.session.delete(user)
    #     db.session.commit()

    def post(self):

        try:
            # Extract JSON data from the request's payload
            data = request.json

            # Validate compulsory fields (email, name, password, and confirm_password)
            if not data.get("email"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_EMAIL.description } , AuthenticationAPIErrors.COMPULSORY_EMAIL.status_code
            if not data.get("name"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_NAME.description } , AuthenticationAPIErrors.COMPULSORY_NAME.status_code
            if not data.get("username"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_USERNAME.description } , AuthenticationAPIErrors.COMPULSORY_USERNAME.status_code
            if not username_pattern.match(data.get("username")):
                return {"msg" : AuthenticationAPIErrors.INVALID_USERNAME.description } , AuthenticationAPIErrors.INVALID_USERNAME.status_code
            if not (data.get("password") and data.get("confirm_password")):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_PASSWORD.description } , AuthenticationAPIErrors.COMPULSORY_PASSWORD.status_code
            if data.get("password") != data.get("confirm_password"):
                return {"msg" : AuthenticationAPIErrors.PASSWORD_NOT_MATCH.description } , AuthenticationAPIErrors.PASSWORD_NOT_MATCH.status_code
            
            # Validate the level field against allowed user levels
            if data.get("level") not in USER_LEVELS_ALLOWED:
                return {"msg" : AuthenticationAPIErrors.LEVEL_NOT_ACCEPTED.description } , AuthenticationAPIErrors.LEVEL_NOT_ACCEPTED.status_code

            # Check if a user with the same email and or username already exists in the database
            flag1 = User.query.filter_by(email=data.get("email")).first()
            flag2 = User.query.filter_by(username=data.get("username")).first()
            
            if flag1:
                return {"msg" : f"{AuthenticationAPIErrors.USER_EXIST.description}-email is duplicate" } , AuthenticationAPIErrors.USER_EXIST.status_code
            elif flag2:
                return {"msg" : f"{AuthenticationAPIErrors.USER_EXIST.description}-username is duplicate" } , AuthenticationAPIErrors.USER_EXIST.status_code
            else:
                # If the user does not exist, create a new user object and add it to the database
                del(data["confirm_password"])
                data["password"] = generate_password_hash(data["password"])
                
                new_user = User(**data,role="student")

                # Add the new user object to the database session and commit the changes
                db.session.add(new_user)
                
                # with open("templates/welcome_user.html") as file_:
                #     template= Template(file_.read())
                #     message = template.render(user_name=data.get("username"))
                #     send_mail.delay(data.get("email"),subject="Welcome to our Platform!",message=message)

                db.session.commit()
                # Return a JSON response with a success message indicating that the user was created
                return {"msg": "User created"},200
        except Exception as e:
            print(e)
            return {"msg" : AuthenticationAPIErrors.INTERNAL_ERROR.description } , AuthenticationAPIErrors.INTERNAL_ERROR.status_code

class AdminRegisterAPI(Resource):
    """
    API endpoint for registering new admin users.

    This class handles HTTP POST requests to register new admin users.

    Methods:
        post(): Handles the HTTP POST request for registering a new admin user.

    Required Data in JSON Payload:
        The HTTP POST request to this endpoint must include the following data\n
        in JSON format:\n
        {\n
            "email": "admin_email@example.com",                            # Admin's email (string)\n
            "password": "password123",                                     # Admin's password (string)\n
            "confirm_password": "password123",                             # Admin's password for confirmation (string)\n
            "name": "John Doe",                                            # Admin's full name (string)\n
            "username" : "JohnDoe"
            "level": "SupportStaff",                                       # Admin's role/level (string)\n
            "github_link": "https://github.com/johndoe",                   # Link to admin's GitHub profile (string, optional)\n
            "linkedin_link": "https://www.linkedin.com/in/johndoe"         # Link to admin's LinkedIn profile (string, optional)\n
        }\n

    Example Usage:
        To register a new admin user, make an HTTP POST request to the API endpoint
        provided by this class with the required admin information in JSON format.
    """

    @jwt_required()
    @roles_accepted(["super admin"])
    def post(self):
        try:
            data = request.json

            # Validate compulsory fields (email, name, password, and confirm_password)
            if not data.get("email"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_EMAIL.description } , AuthenticationAPIErrors.COMPULSORY_EMAIL.status_code
            if not data.get("name"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_NAME.description } , AuthenticationAPIErrors.COMPULSORY_NAME.status_code
            if not data.get("username"):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_USERNAME.description } , AuthenticationAPIErrors.COMPULSORY_USERNAME.status_code
            if not (data.get("password") and data.get("confirm_password")):
                return {"msg" : AuthenticationAPIErrors.COMPULSORY_PASSWORD.description } , AuthenticationAPIErrors.COMPULSORY_PASSWORD.status_code
            if data.get("password") != data.get("confirm_password"):
                return {"msg" : AuthenticationAPIErrors.PASSWORD_NOT_MATCH.description } , AuthenticationAPIErrors.PASSWORD_NOT_MATCH.status_code
            
            # Validate the level field against allowed user levels
            if data.get("level") not in ADMIN_LEVELS_ALLOWED:
                return {"msg" : AuthenticationAPIErrors.LEVEL_NOT_ACCEPTED.description } , AuthenticationAPIErrors.LEVEL_NOT_ACCEPTED.status_code

            # Check if a user with the same email and or username already exists in the database
            flag1 = User.query.filter_by(email=data.get("email")).first()
            flag2 = User.query.filter_by(username=data.get("username")).first()
            
            if flag1:
                return {"msg" : f"{AuthenticationAPIErrors.USER_EXIST.description}-email is duplicate" } , AuthenticationAPIErrors.USER_EXIST.status_code
            elif flag2:
                return {"msg" : f"{AuthenticationAPIErrors.USER_EXIST.description}-username is duplicate" } , AuthenticationAPIErrors.USER_EXIST.status_code
            else:
                # If the user does not exist, create a new user object and add it to the database
                del(data["confirm_password"])
                data["password"] = generate_password_hash(data["password"])
                
                new_user = User(**data,role="admin")

                # Add the new user object to the database session and commit the changes
                db.session.add(new_user)
                db.session.commit()
                with open("templates/welcome_user.html") as file_:
                    template= Template(file_.read())
                    message = template.render(user_name=data.get("username"))
                    send_mail.delay(data.get("email"),subject="Welcome to our Platform!",message=message)
                # Return a JSON response with a success message indicating that the user was created
                return {"msg": "Admin created"},200
        except Exception as e:
            print(e)
            return {"msg" : AuthenticationAPIErrors.INTERNAL_ERROR.description } , AuthenticationAPIErrors.INTERNAL_ERROR.status_code

class LoginAPI(Resource):
    """
    API endpoint for user login.

    This class handles HTTP POST requests for user login.

    Methods:
        post(): Handles the HTTP POST request for user login.

    Required Data in JSON Payload:    
        The HTTP POST request to this endpoint must include the following data    
        in JSON format:\n    
        {\n
            "email": "user_email@example.com",                             # User's email (string)\n
            "password": "user_password"                                    # User's password (string)\n 
        }\n   

    Example Usage:
        To log in a user, make an HTTP POST request to the API endpoint
        provided by this class with the user's login credentials in JSON format.
    """
    def post(self):
        try:
            data = request.json

            # Find the user with the provided email in the database
            curr_user = User.query.filter_by(email=data.get("email")).first()

            # Check if the user exists and the password is correct and user is not blocked
            if curr_user:
                if not curr_user.active:
                    return {"msg" : AuthenticationAPIErrors.USER_BLOCKED.description } , AuthenticationAPIErrors.USER_BLOCKED.status_code

                if check_password_hash(curr_user.password, data.get("password")):
                    # Generate an access token for the user's identity
                    access_token = create_access_token(identity={
                        "id": curr_user.id,
                        "email": curr_user.email
                    })

                    # Prepare the response data with access token and user information
                    response_data = {
                        "message": "Logged in successfully",
                        "access_token": access_token,
                        "name": curr_user.name,
                        "role": curr_user.role,
                        "user_id":curr_user.id
                    }

                    # Return the response data as a JSON response
                    print(response_data)
                    return jsonify(response_data)
                else:
                    # If the credentials are invalid, return a 403 Forbidden status code with an error message
                    return {"msg" : AuthenticationAPIErrors.INVALID_DATA.description } , AuthenticationAPIErrors.INVALID_DATA.status_code
            else:
                # If the credentials are invalid, return a 403 Forbidden status code with an error message
                return {"msg" : AuthenticationAPIErrors.INVALID_DATA.description } , AuthenticationAPIErrors.INVALID_DATA.status_code

        except Exception as e:
            return {"msg" : AuthenticationAPIErrors.INTERNAL_ERROR.description } , AuthenticationAPIErrors.INTERNAL_ERROR.status_code


class VerifyToken(Resource):
    @jwt_required()
    def get(self):
        try:
            user_identity = get_jwt_identity()
            user_id = user_identity.get("id")
            
            curr_user = User.query.filter_by(id=user_id).first()

            data = {
                "name": curr_user.name,
                "role": curr_user.role,
                "user_id":user_id
            }
            print(data)
            return jsonify(data)    
        except Exception as e:
            return {"msg" : AuthenticationAPIErrors.INTERNAL_ERROR.description } , AuthenticationAPIErrors.INTERNAL_ERROR.status_code



