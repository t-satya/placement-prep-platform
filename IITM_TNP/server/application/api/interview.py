from flask import jsonify,request,abort
from flask_restful import Resource
from application.models import User,Interviews
from application.database import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,get_jwt_identity
from utils.roles_accepted import roles_accepted
from utils.error_codes import InterviewAPIErrors
from utils.constants import JOB_TYPE_ALLOWED

class InterviewAPI(Resource):
    def get(self):
        """
        Retrieve all interviews.

        Returns:
            dict: A dictionary containing the message indicating success or error, 
                along with a list of interview data if successful.
        """
        try:
            payload = []
            interviews = Interviews.query.all()

            for interview in interviews:
                data = {
                    "id" : interview.id,
                    "company" : interview.company,
                    "job_role" : interview.job_role,
                    "job_type" : interview.job_type,
                    "description" : interview.description,
                    "user_name" : interview.created_by.name if not interview.anonymous else "Anonymous"
                }
                payload.append(data)

            print(payload)
            return {"msg" : "Success", "interviews" : payload}
        
        except Exception as e:
            return {"msg" : InterviewAPIErrors.INTERNAL_ERROR.description } , InterviewAPIErrors.INTERNAL_ERROR.status_code


    @jwt_required()
    def post(self):
        """
        Required Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "company": "Amazon",                                    # Company's Name (string)\n
                "job_role": "SDE",                                      # Job role(string)\n
                "job_type": "Internship",                               # Job type(string)\n
                "anonymous": "True",                                    # Is User Identity Anonumous (boolean)\n
                "description": "Interview was fantastic",               # Description of interview experience (string)\n
            }\n

       """
        try:
            user = get_jwt_identity()
            # Extract JSON data from the request's payload
            data = request.json

            # Validate the incoming data
            if not data.get("company"):
                return {"msg" : InterviewAPIErrors.COMPULSORY_COMPANY_NAME.description } , InterviewAPIErrors.COMPULSORY_COMPANY_NAME.status_code
            if not data.get("job_role"):
                return {"msg" : InterviewAPIErrors.COMPULSORY_JOB_ROLE.description } , InterviewAPIErrors.COMPULSORY_JOB_ROLE.status_code
            if not data.get("job_type"):
                return {"msg" : InterviewAPIErrors.COMPULSORY_JOB_TYPE.description } , InterviewAPIErrors.COMPULSORY_JOB_TYPE.status_code
            if not data.get("job_type") in JOB_TYPE_ALLOWED:
                return {"msg" : InterviewAPIErrors.INVALID_JOB_TYPE.description } , InterviewAPIErrors.INVALID_JOB_TYPE.status_code
            if not data.get("description"):
                return {"msg" : InterviewAPIErrors.DESCRIPTION_REQUIRED.description } , InterviewAPIErrors.DESCRIPTION_REQUIRED.status_code

            # Create the interview and add it to database
            interview = Interviews(**data, user_id=user.get("id"))
            db.session.add(interview)
            db.session.commit()

            return {"msg": "Interview created"} , 200
        except Exception as e:
            print(e)
            return {"msg" : InterviewAPIErrors.INTERNAL_ERROR.description } , InterviewAPIErrors.INTERNAL_ERROR.status_code

    @jwt_required()
    def put(self):
        """
        Expected Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "interview_id" : 2,                                     # Id of interview to edit (int)\n
                "company": "Amazon",                                    # Company's Name (string)\n
                "job_role": "SDE",                                      # Job role(string)\n
                "job_type": "Internship",                               # Job type(string)\n
                "anonymous": "True",                                    # Is User Identity Anonumous (boolean)\n
                "description": "Interview was fantastic",               # Description of interview experience (string)\n
            }\n

       """
        
        try:
            user = get_jwt_identity()

            # Extract JSON data from the request's payload
            data = request.json

            # Validate the incoming data
            if not data.get("interview_id"):
                return {"msg" : InterviewAPIErrors.INTERVIEW_ID_REQUIRED.description } , InterviewAPIErrors.INTERVIEW_ID_REQUIRED.status_code
            
            interview = Interviews.query.filter_by(id=data.get("interview_id"),user_id=user.get("id")).first()

            if not interview:
                return {"msg" : InterviewAPIErrors.INTERVIEW_NOT_FOUND.description } , InterviewAPIErrors.INTERVIEW_NOT_FOUND.status_code
            
            if data.get("company"):
                interview.company = data.get("company")
            
            if data.get("job_role"):
                print("Yaah")
                interview.job_role = data.get("job_role")

            if data.get("job_type"):
                if data.get("job_type") in JOB_TYPE_ALLOWED:
                    interview.job_type = data.get("job_type")
                else:
                    return {"msg" : InterviewAPIErrors.INVALID_JOB_TYPE.description } , InterviewAPIErrors.INVALID_JOB_TYPE.status_code

            if data.get("anonymous")=="False":
                interview.anonymous = False
            elif data.get("anonymous")=="True":
                interview.anonymous = True

            if data.get("description"):
                interview.description = data.get("description")

            db.session.commit()

            return {"msg": "Interview updated"} , 200
        except Exception as e:
            print(e)
            return {"msg" : InterviewAPIErrors.INTERNAL_ERROR.description } , InterviewAPIErrors.INTERNAL_ERROR.status_code

    @jwt_required()
    def delete(self,id=None):
        try:
            print(id)
            user = get_jwt_identity()

            interview = Interviews.query.filter_by(id=id,user_id=user.get("id")).first()
            if not interview:
                    return {"msg" : InterviewAPIErrors.INTERVIEW_NOT_FOUND.description } , InterviewAPIErrors.INTERVIEW_NOT_FOUND.status_code
            
            db.session.delete(interview)
            db.session.commit()

            return {"msg": "Interview deleted"} , 200
        except Exception as e:
            print(e)
            return {"msg" : InterviewAPIErrors.INTERNAL_ERROR.description } , InterviewAPIErrors.INTERNAL_ERROR.status_code

