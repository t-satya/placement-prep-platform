from flask import jsonify,request,abort
from flask_restful import Resource
from application.models import PracticeTests,Questions,ques_practice
from application.database import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import jwt_required,create_access_token
from utils.roles_accepted import roles_accepted
from utils.error_codes import PracticeTestAPIErrors
from utils.constants import USER_LEVELS_ALLOWED, ADMIN_LEVELS_ALLOWED

class PracticeTestAPI(Resource):

    @jwt_required()
    def get(self,id=None):
        try:
            if id:
                payload = {}
                practice_test = PracticeTests.query.filter_by(id=id).first()

                if not practice_test:
                    return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_NOT_FOUND.description } , PracticeTestAPIErrors.PRACTICE_TEST_NOT_FOUND.status_code

                payload["id"] = practice_test.id
                payload["name"] = practice_test.name
                payload["tags"] = practice_test.tags

                questions = []
                for question in practice_test.questions:
                    data = {
                        "id" : question.id,
                        "name" : question.name,
                        "tags" : question.tags,
                        "description" : question.description,
                        "question_type" : question.question_type,
                        "options" : question.options if question.question_type in ['MCQ','MSQ'] else None,
                        "correct_answers" : question.correct_answers if question.question_type in ['MCQ','MSQ','NAT'] else None
                    }
                    questions.append(data)
                payload["questions"] = questions
                return {"msg" : "Success", "practice_tests" : payload}
            else:
                payload = []
                practice_tests = PracticeTests.query.all()

                for practice_test in practice_tests:
                    data = {
                        "id" : practice_test.id,
                        "name" : practice_test.name,
                        "tags" : practice_test.tags
                    }

                    payload.append(data)
                return {"msg" : "Success", "practice_tests" : payload}
        except Exception as e:
            print(e)
            return {"msg" : PracticeTestAPIErrors.INTERNAL_ERROR.description } , PracticeTestAPIErrors.INTERNAL_ERROR.status_code


    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def post(self):
        """
        {
            "name" : "" \n
            "tags" : [] \n
            "question_ids" : [] \n
        }
        """
        try:
            data = request.json

            # Validate the incoming data
            if not data.get("name"):
                return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_NAME_REQUIRED.description } , PracticeTestAPIErrors.PRACTICE_TEST_NAME_REQUIRED.status_code

            test = PracticeTests.query.filter_by(name=data.get("name")).first()
            if test :
                return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_EXISTS.description}, PracticeTestAPIErrors.PRACTICE_TEST_EXISTS.status_code

            if not data.get("tags"):
                return {"msg" : PracticeTestAPIErrors.TAGS_REQUIRED.description } , PracticeTestAPIErrors.TAGS_REQUIRED.status_code
            if not isinstance(data.get("tags"), list):
                return {"msg" : PracticeTestAPIErrors.INVALID_TAGS.description } , PracticeTestAPIErrors.INVALID_TAGS.status_code
            if len(list(data.get("tags")))==0:
                return {"msg" : PracticeTestAPIErrors.INVALID_TAGS.description } , PracticeTestAPIErrors.INVALID_TAGS.status_code
            
            if not data.get("question_ids"):
                return {"msg" : PracticeTestAPIErrors.QUESTION_IDS_REQUIRED.description } , PracticeTestAPIErrors.QUESTION_IDS_REQUIRED.status_code
            if not isinstance(data.get("question_ids"), list):
                return {"msg" : PracticeTestAPIErrors.QUESTION_IDS_INVALID.description } , PracticeTestAPIErrors.QUESTION_IDS_INVALID.status_code
            if len(list(data.get("question_ids")))<5:
                return {"msg" : PracticeTestAPIErrors.QUESTION_IDS_LENGTH.description } , PracticeTestAPIErrors.QUESTION_IDS_LENGTH.status_code

            practice_test = PracticeTests(name=data.get("name"),tags = data.get("tags"))
            ques_ids=[int(j) for j in data.get("question_ids")]
            
            for id in ques_ids:
                each_question = Questions.query.filter_by(id=id).first()
                if not each_question:
                    db.session.rollback()
                    return {"msg" : f"{PracticeTestAPIErrors.QUESTION_NOT_FOUND.description}-question_id={id}"},PracticeTestAPIErrors.QUESTION_NOT_FOUND.status_code
                practice_test.questions.append(each_question)
                            
            db.session.add(practice_test)
            db.session.commit()

            return {"msg": "Practice Test created"} , 200

        except Exception as e:
            print(e)
            return {"msg" : PracticeTestAPIErrors.INTERNAL_ERROR.description } , PracticeTestAPIErrors.INTERNAL_ERROR.status_code

    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def put(self):
        """
        {
            "practice_test_id" : ""\n
            "name" : "" \n
            "tags" : [] \n
            "question_ids_to_remove" : [] \n
            "question_ids_to_add" : [] \n
        }
        """
        try:
            # Extract JSON data from the request's payload
            data = request.json

            # Validate the incoming data
            if not data.get("practice_test_id"):
                return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_ID_REQUIRED.description } , PracticeTestAPIErrors.PRACTICE_TEST_ID_REQUIRED.status_code
            
            practice_test = PracticeTests.query.filter_by(id=data.get("practice_test_id")).first()

            if not practice_test:
                return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_NOT_FOUND.description } , PracticeTestAPIErrors.PRACTICE_TEST_NOT_FOUND.status_code
            
            if data.get("name"):
                test = PracticeTests.query.filter_by(name=data.get("name")).first()
                if test :
                    return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_EXISTS.description}, PracticeTestAPIErrors.PRACTICE_TEST_EXISTS.status_code
                practice_test.name = data.get("name")

            if data.get("tags"):
                if not isinstance(data.get("tags"), list):
                    return {"msg" : PracticeTestAPIErrors.INVALID_TAGS.description } , PracticeTestAPIErrors.INVALID_TAGS.status_code
                if len(list(data.get("tags")))==0:
                    return {"msg" : PracticeTestAPIErrors.INVALID_TAGS.description } , PracticeTestAPIErrors.INVALID_TAGS.status_code
                practice_test.tags = data.get("tags")

            if data.get("question_ids_to_remove"):
                if not isinstance(data.get("question_ids_to_remove"), list):
                    return {"msg" : PracticeTestAPIErrors.QUESTION_IDS_INVALID.description } , PracticeTestAPIErrors.QUESTION_IDS_INVALID.status_code
                else:
                    for id in data.get("question_ids_to_remove"):
                        ques = Questions.query.filter_by(id=id).first()
                        if ques:
                            practice_test.questions.remove(ques)

            if data.get("question_ids_to_add"):
                if not isinstance(data.get("question_ids_to_add"), list):
                    return {"msg" : PracticeTestAPIErrors.QUESTION_IDS_INVALID.description } , PracticeTestAPIErrors.QUESTION_IDS_INVALID.status_code
                else:
                    for id in data.get("question_ids_to_add"):
                        ques = Questions.query.filter_by(id=id).first()
                        if not ques:
                            db.session.rollback()
                            return {"msg" : f"{PracticeTestAPIErrors.QUESTION_NOT_FOUND.description}-question_id={id}"},PracticeTestAPIErrors.QUESTION_NOT_FOUND.status_code
                        practice_test.questions.append(ques)
            
            if len(practice_test.questions)<5:
                db.session.rollback()
                return {"msg" : f"{PracticeTestAPIErrors.QUESTION_IDS_LENGTH.description}. So could not add and/or remove questions" } , PracticeTestAPIErrors.QUESTION_IDS_LENGTH.status_code

            db.session.commit()

            return {"msg" : "Practice test updated"},200

        except Exception as e:
            print(e)
            return {"msg" : PracticeTestAPIErrors.INTERNAL_ERROR.description } , PracticeTestAPIErrors.INTERNAL_ERROR.status_code


    @jwt_required()
    @roles_accepted(['admin','super admin'])
    def delete(self,id=None):
        try:
            practice_test = PracticeTests.query.filter_by(id=id).first()
            if not practice_test:
                return {"msg" : PracticeTestAPIErrors.PRACTICE_TEST_NOT_FOUND.description } , PracticeTestAPIErrors.PRACTICE_TEST_NOT_FOUND.status_code
            
            db.session.delete(practice_test)
            db.session.commit()

            return {"msg": "Practice test deleted"} , 200
        except Exception as e:
            print(e)
            return {"msg" : PracticeTestAPIErrors.INTERNAL_ERROR.description } , PracticeTestAPIErrors.INTERNAL_ERROR.status_code
        
