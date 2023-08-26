from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from utils.error_codes import PostsRepliesAPIErrors
from application.models import Replies,Posts
from application.database import db
from datetime import datetime
class RepliesAPI(Resource):

    @jwt_required()
    def post(self):
        data = request.json
        """
        Required Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "description": "I like your post here's something I want to add to it", # Body of the reply goes in here \n                                    # Company's Name (string)\n
                "postid":"2"
            }\n

       """
        try:
            curr_user = get_jwt_identity()
            data = request.json
            if not data.get("description"):
                return {"msg" : PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.description } , PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            if not data.get("postid"):
                return {"msg": PostsRepliesAPIErrors.POSTID_REQUIRED.description}, PostsRepliesAPIErrors.POSTID_REQUIRED.status_code
            post_obj=Posts.query.filter_by(id=data.get("postid")).first()
            if not post_obj:
                return {"msg": PostsRepliesAPIErrors.POSTID_INVALID.description}, PostsRepliesAPIErrors.POSTID_INVALID.status_code
            
            new_reply = Replies(
                description = data.get("description"),
                user_id = curr_user.get("id"),
                post_id = int(data.get("postid")),
                timestamp = datetime.today()
            )
            db.session.add(new_reply)
            db.session.commit()
            return {"msg":"Replied to the post successfully"}
            

        except Exception as e:
            print(e)
            return {"msg" : PostsRepliesAPIErrors.INTERNAL_ERROR.description } , PostsRepliesAPIErrors.INTERNAL_ERROR.status_code
    
    @jwt_required()
    def put(self,replyid):
        data = request.json
        """
        Required Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "description": "I like your post here's something I want to add to it", # Body of the reply goes in here \n                                    # Company's Name (string)\n
            }\n

       """
        try:
            curr_user = get_jwt_identity()
            data = request.json
            if not data.get("description"):
                return {"msg" : PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.description } , PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            reply_obj=Replies.query.filter_by(id=replyid).first()
            if not reply_obj:
                return {"msg": PostsRepliesAPIErrors.POSTID_INVALID.description}, PostsRepliesAPIErrors.POSTID_INVALID.status_code
            if curr_user.get("id")!=reply_obj.user_id:
                return {"msg" : PostsRepliesAPIErrors.INVALID_EDIT.description } , PostsRepliesAPIErrors.INVALID_EDIT.status_code
           
            reply_obj.description=data.get("description")
            db.session.commit()
            return {"msg":"Reply edited"}
            

        except Exception as e:
            print(e)
            return {"msg" : PostsRepliesAPIErrors.INTERNAL_ERROR.description } , PostsRepliesAPIErrors.INTERNAL_ERROR.status_code



    @jwt_required()
    def delete(self,replyid):
        try:
            curr_user = get_jwt_identity()
            reply_obj = Replies.query.filter_by(id=replyid).first()

            if curr_user.get("id")!=reply_obj.user_id:
                if curr_user.get("role")!="admin":
                    if curr_user.get("role")!="super admin":
                        return {"msg" : PostsRepliesAPIErrors.INVALID_EDIT.description } , PostsRepliesAPIErrors.INVALID_EDIT.status_code
            if not reply_obj:
                return {"msg": PostsRepliesAPIErrors.POSTID_INVALID.description}, PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            
            db.session.delete(reply_obj)
            db.session.commit()
            return {"msg":"Reply Deleted"}
            
        except Exception as e:
            print(e)
            return {"msg" : PostsRepliesAPIErrors.INTERNAL_ERROR.description } , PostsRepliesAPIErrors.INTERNAL_ERROR.status_code
        