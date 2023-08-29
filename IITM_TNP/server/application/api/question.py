from flask import jsonify,request,abort
from flask_restful import Resource
from application.models import Questions
from application.database import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,get_jwt_identity
from utils.roles_accepted import roles_accepted
from utils.error_codes import QuestionAPIErrors
from utils.constants import QUESTION_TYPE_ALLOWED

class QuestionAPI(Resource):
    
    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def get(self):
        try:
            payload = []
            questions = Questions.query.all()

            for question in questions:
                data = {
                    "id" : question.id,
                    "name" : question.name,
                    "tags" : question.tags,
                    "description" : question.description,
                    "question_type" : question.question_type,
                    "options" : question.options if question.question_type in ['MCQ','MSQ'] else None,
                    "correct_answers" : question.correct_answers if question.question_type in ['MCQ','MSQ','NAT'] else None
                }
                payload.append(data)

            # print(payload)
            return {"msg" : "Success", "questions" : payload}
        
        except Exception as e:
            return {"msg" : QuestionAPIErrors.INTERNAL_ERROR.description } , QuestionAPIErrors.INTERNAL_ERROR.status_code


    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def post(self):
        """
        Required Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "name": "Water Image 1", \n                                
                "tags": "["Maths","Reasoning]" \n                                     
                "description": "Identify water image",\n                      
                "question_type": "MCQ",                 \n                   
                "options": "{"1":"A","2":B,"3":"C","4":"D"}",\n               
                "correct_answers" : "["1"]"\n
            }\n

       """
        try:
            # Extract JSON data from the request's payload
            data = request.json

            # Validate the incoming data
            if not data.get("name"):
                return {"msg" : QuestionAPIErrors.COMPULSORY_QUESTION_NAME.description } , QuestionAPIErrors.COMPULSORY_QUESTION_NAME.status_code
            
            ques = Questions.query.filter_by(name=data.get("name")).first()
            if ques:
                return {"msg" : QuestionAPIErrors.QUESTION_EXISTS.description } , QuestionAPIErrors.QUESTION_EXISTS.status_code
            if not data.get("tags"):
                return {"msg" : QuestionAPIErrors.TAGS_REQUIRED.description } , QuestionAPIErrors.TAGS_REQUIRED.status_code
            if not isinstance(data.get("tags"), list):
                return {"msg" : QuestionAPIErrors.INVALID_TAGS.description } , QuestionAPIErrors.INVALID_TAGS.status_code
            if len(list(data.get("tags")))==0:
                return {"msg" : QuestionAPIErrors.INVALID_TAGS.description } , QuestionAPIErrors.INVALID_TAGS.status_code
            if not data.get("description"):
                return {"msg" : QuestionAPIErrors.DESCRIPTION_REQUIRED.description } , QuestionAPIErrors.DESCRIPTION_REQUIRED.status_code
            if not data.get("question_type"):
                return {"msg" : QuestionAPIErrors.QUESTION_TYPE_REQUIRED.description } , QuestionAPIErrors.QUESTION_TYPE_REQUIRED.status_code
            if not data.get("question_type") in QUESTION_TYPE_ALLOWED:
                return {"msg" : QuestionAPIErrors.INVALID_QUESTION_TYPE.description } , QuestionAPIErrors.INVALID_QUESTION_TYPE.status_code

            
            if data.get("question_type")  in ['MCQ', 'MSQ']:
                if not isinstance(data.get("options"), dict):
                    return {"msg" : QuestionAPIErrors.INVALID_OPTIONS.description}, QuestionAPIErrors.INVALID_OPTIONS.status_code
                elif not has_required_keys(data.get("options")):
                    return {"msg" : QuestionAPIErrors.OPTIONS_REQUIRED.description}, QuestionAPIErrors.OPTIONS_REQUIRED.status_code

            if data.get("question_type")  in ['MCQ', 'MSQ', 'NAT']:
                if not isinstance(data.get("correct_answers"), list):
                    return {"msg" : QuestionAPIErrors.INVALID_ANSWER.description}, QuestionAPIErrors.INVALID_ANSWER.status_code
                elif len(list(data.get("correct_answers")))==0:
                    return {"msg" : QuestionAPIErrors.ANSWER_REQUIRED.description}, QuestionAPIErrors.ANSWER_REQUIRED.status_code

                elif data.get("question_type") != 'NAT' and not set(data.get("correct_answers")).issubset(data.get("options").keys()):
                    return {"msg" : QuestionAPIErrors.ANSWER_REQUIRED.description}, QuestionAPIErrors.ANSWER_REQUIRED.status_code

            if data.get("question_type") in ['NAT','Coding']:
                data["options"] = {}
            
            if data.get("question_type") in ['Coding']:
                data["correct_answers"] = []

            # Create the question and add it to database
            ques = Questions(**data)
            db.session.add(ques)
            db.session.commit()

            return {"msg": "Question created"} , 200
        except Exception as e:
            print(e)
            return {"msg" : QuestionAPIErrors.INTERNAL_ERROR.description } , QuestionAPIErrors.INTERNAL_ERROR.status_code

    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def put(self):
        """
        Expected Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "question_id: : "2"
                "name": "Water Image 1", \n                                
                "tags": "["Maths","Reasoning]" \n                                     
                "description": "Identify water image",\n                      
                "question_type": "MCQ",                 \n                   
                "options": "{"1":"A","2":B,"3":"C","4":"D"}",\n               
                "correct_answers" : "["1"]"\n
            }\n
        """
        
        try:
            # Extract JSON data from the request's payload
            data = request.json

            # Validate the incoming data
            if not data.get("question_id"):
                return {"msg" : QuestionAPIErrors.QUESTION_ID_REQUIRED.description } , QuestionAPIErrors.QUESTION_ID_REQUIRED.status_code
            
            question = Questions.query.filter_by(id = data.get("question_id")).first()
            if not question:
                return {"msg" : QuestionAPIErrors.QUESTION_NOT_FOUND.description } , QuestionAPIErrors.QUESTION_NOT_FOUND.status_code
            
            if data.get("name"):
                question.name = data.get("name")
            
            if data.get("tags"):
                question.tags = data.get("tags")

            if data.get("description"):
                question.description = data.get("description")

            if data.get("question_type"):
                if data.get("question_type")  in ['MCQ', 'MSQ']:
                    if not isinstance(data.get("options"), dict):
                        return {"msg" : QuestionAPIErrors.INVALID_OPTIONS.description}, QuestionAPIErrors.INVALID_OPTIONS.status_code
                    elif not has_required_keys(data.get("options")):
                        return {"msg" : QuestionAPIErrors.OPTIONS_REQUIRED.description}, QuestionAPIErrors.OPTIONS_REQUIRED.status_code

                if data.get("question_type")  in ['MCQ', 'MSQ', 'NAT']:
                    if not isinstance(data.get("correct_answers"), list):
                        return {"msg" : QuestionAPIErrors.INVALID_ANSWER.description}, QuestionAPIErrors.INVALID_ANSWER.status_code
                    elif len(list(data.get("correct_answers")))==0:
                        return {"msg" : QuestionAPIErrors.ANSWER_REQUIRED.description}, QuestionAPIErrors.ANSWER_REQUIRED.status_code

                    elif data.get("question_type") != 'NAT' and not set(data.get("correct_answers")).issubset(data.get("options").keys()):
                        return {"msg" : QuestionAPIErrors.ANSWER_REQUIRED.description}, QuestionAPIErrors.ANSWER_REQUIRED.status_code

                if data.get("question_type") in ['NAT','Coding']:
                    data["options"] = {}
                    question.options = data["options"]

                
                if data.get("question_type") in ['Coding']:
                    data["correct_answers"] = []
                question.question_type=data.get("question_type")
            
            if data.get("options"):
                if not isinstance(data.get("options"), dict):
                    db.session.rollback()
                    return {"msg" : QuestionAPIErrors.INVALID_OPTIONS.description}, QuestionAPIErrors.INVALID_OPTIONS.status_code
                elif not has_required_keys(data.get("options")):
                    db.session.rollback()
                    return {"msg" : QuestionAPIErrors.OPTIONS_REQUIRED.description}, QuestionAPIErrors.OPTIONS_REQUIRED.status_code
                else:
                    question.options = data.get("options")
            
            if data.get("correct_answers"):
                if not isinstance(data.get("correct_answers"), list):
                    return {"msg" : QuestionAPIErrors.INVALID_ANSWER.description}, QuestionAPIErrors.INVALID_ANSWER.status_code
                elif len(list(data.get("correct_answers")))==0:
                    print(len(list(data.get("correct_answers"))))
                    return {"msg" : QuestionAPIErrors.ANSWER_REQUIRED.description}, QuestionAPIErrors.ANSWER_REQUIRED.status_code

                elif question.question_type != 'NAT' and not set(data.get("correct_answers")).issubset(question.options.keys()):
                    return {"msg" : QuestionAPIErrors.ANSWER_REQUIRED.description}, QuestionAPIErrors.ANSWER_REQUIRED.status_code
                else:
                    question.correct_answers = data.get("correct_answers")

            db.session.commit()

            return {"msg": "Question updated"} , 200
        except Exception as e:
            print(e)
            return {"msg" : QuestionAPIErrors.INTERNAL_ERROR.description } , QuestionAPIErrors.INTERNAL_ERROR.status_code

    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def delete(self,id=None):
        try:
            ques = Questions.query.filter_by(id=id).first()
            if not ques:
                return {"msg" : QuestionAPIErrors.QUESTION_NOT_FOUND.description } , QuestionAPIErrors.QUESTION_NOT_FOUND.status_code
            
            db.session.delete(ques)
            db.session.commit()

            return {"msg": "Question deleted"} , 200
        except Exception as e:
            print(e)
            return {"msg" : QuestionAPIErrors.INTERNAL_ERROR.description } , QuestionAPIErrors.INTERNAL_ERROR.status_code
        





def has_required_keys(dictionary):
    required_keys = {"1", "2", "3", "4"}
    return required_keys.issubset(dictionary.keys())