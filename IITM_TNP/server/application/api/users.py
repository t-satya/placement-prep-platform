from flask import jsonify,request,abort
from flask_restful import Resource
from application.models import User
from application.database import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,get_jwt_identity
from utils.roles_accepted import roles_accepted
from utils.error_codes import UsersAPIErrors
from utils.constants import USER_LEVELS_ALLOWED, ADMIN_LEVELS_ALLOWED

class UsersAPI(Resource):

    def get(self,id=None):
        """
            Get user's data for dashboard
        """
        try:
            user = User.query.filter_by(id = id).first()
            
            if not user:
                return {"msg" : UsersAPIErrors.USER_NOT_EXIST.description } , UsersAPIErrors.USER_NOT_EXIST.status_code

            payload = {}
            payload["email"] = user.email
            payload["name"] = user.name
            payload["username"] = user.username
            payload["level"] = user.level
            payload["github_link"] = user.github_link
            payload["linkedin_link"] = user.linkedin_link
            print(payload)
            return {"msg" : "Success", "user" : payload},200
        except Exception as e:
            print(e)
            return {"msg" : UsersAPIErrors.INTERNAL_ERROR.description } , UsersAPIErrors.INTERNAL_ERROR.status_code


    @jwt_required()
    def put(self):
        """
            User can update his info

            {   "name":"",
                "github_link" : ""\n,
                "linkedin_link" : ""\n
            }
        """
        try:
            # Get the user's identity
            user_identity = get_jwt_identity()

            data = request.json
            user = User.query.filter_by(id = user_identity["id"]).first()

            if data.get("github_link"):
                user.github_link = data.get("github_link")
            if data.get("name"):
                user.name = data.get("name")
            
            if data.get("linkedin_link"):
                user.linkedin_link = data.get("linkedin_link")
            
            db.session.commit()
            return {"msg" : "Updated Successfully"},200

        except Exception as e:
            print(e)
            return {"msg" : UsersAPIErrors.INTERNAL_ERROR.description } , UsersAPIErrors.INTERNAL_ERROR.status_code

    @jwt_required()
    @roles_accepted(["super admin"])
    def patch(self):
        """
            Admin can block a users
            {   
                "user_id" : "" \n
                "block" : "" \n # Either yes or no
            }
        """
        try:
            data = request.json
            user = User.query.filter_by(id = data.get("user_id")).first()
            
            if not user:
                return {"msg" : UsersAPIErrors.USER_NOT_EXIST.description } , UsersAPIErrors.USER_NOT_EXIST.status_code

            if data.get("block"):
                if data.get("block")=="yes":
                    user.active = False
                elif data.get("block")=="no":
                    user.active=True

            db.session.commit()
            return {"msg" : "Updated Successfully"},200
        
        except Exception as e:
            print(e)
            return {"msg" : UsersAPIErrors.INTERNAL_ERROR.description } , UsersAPIErrors.INTERNAL_ERROR.status_code
