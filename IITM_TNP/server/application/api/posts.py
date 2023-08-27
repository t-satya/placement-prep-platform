from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from utils.error_codes import PostsRepliesAPIErrors
from application.models import Posts
from application.database import db
from datetime import datetime


class PostsAPI(Resource):

    @jwt_required()
    def get(self):
        """
        Retrieve all posts.

        Returns:
            dict: A dictionary containing the message indicating success or error, 
                along with a list of posts data if successful.
                Each post also has a list of replies.
        """
        payload=[]
        all_posts = Posts.query.all()

        for eachpost in all_posts:
            post_replies=[]
            for eachreply in eachpost.replies:
                reply={
                    "id":eachreply.id,
                    "username":eachreply.replied_by.username,
                    "description":eachreply.description,
                    "timestamp":str(eachreply.timestamp),
                    "user_id":eachreply.user_id
                }
                post_replies.append(reply)
            data={
                "id":eachpost.id,
                "username":eachpost.posted_by.username,
                "description":eachpost.description,
                "tags":eachpost.tags,
                "timestamp":str(eachpost.timestamp),
                "replies":post_replies,
                "user_id":eachpost.user_id
            }
            payload.append(data)
        print(payload)
        return {"msg":"Success","all_posts":payload}

    @jwt_required()
    def post(self):
        """
        Required Data in JSON Payload:
            The HTTP POST request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "description": "I need some advice on how to get started with ML projects", # Body of the post goes in here \n                                    # Company's Name (string)\n
                "tags": ["Machine Learning","Advice"],                                      # User can add any tags associated with each post\n
            }\n

       """
        try:
            curr_user = get_jwt_identity()
            data = request.json
            if not data.get("description"):
                return {"msg" : PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.description } , PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            if not data.get("tags"):
                return {"msg" : PostsRepliesAPIErrors.TAGS_REQUIRED.description } , PostsRepliesAPIErrors.TAGS_REQUIRED.status_code
            if not isinstance(data.get("tags"), list):
                return {"msg" : PostsRepliesAPIErrors.INVALID_TAGS.description } , PostsRepliesAPIErrors.INVALID_TAGS.status_code
            if len(list(data.get("tags")))==0:
                return {"msg" : PostsRepliesAPIErrors.INVALID_TAGS.description } , PostsRepliesAPIErrors.INVALID_TAGS.status_code
            new_post = Posts(
                description = data.get("description"),
                tags = data.get("tags"),
                user_id = curr_user["id"],
                timestamp = datetime.today()

            )
            db.session.add(new_post)
            db.session.commit()
            return {"msg":"Posted successfully"}
            

        except Exception as e:
            print(e)
            return {"msg" : PostsRepliesAPIErrors.INTERNAL_ERROR.description } , PostsRepliesAPIErrors.INTERNAL_ERROR.status_code
        
    @jwt_required()
    def put(self,postid):
        """
        Required Data in JSON Payload:
            The HTTP PUT request to this endpoint must include the following data\n
            in JSON format:\n
            {
                "description": "I need some advice on how to get started with ML projects", # Body of the post goes in here \n                                    # Company's Name (string)\n
                "tags": ["Machine Learning","Advice"],                                      # User can add any tags associated with each post\n
            }\n

       """
        try:
            curr_user = get_jwt_identity()
            post_obj=Posts.query.filter_by(id=postid).first()
            data = request.json
           
            if not post_obj:
                return {"msg": PostsRepliesAPIErrors.POSTID_INVALID.description}, PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            if curr_user.get("id")!=post_obj.user_id:
                return {"msg" : PostsRepliesAPIErrors.INVALID_EDIT.description } , PostsRepliesAPIErrors.INVALID_EDIT.status_code
            if not data.get("description"):
                return {"msg" : PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.description } , PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            
            if not isinstance(data.get("tags"), list):
                return {"msg" : PostsRepliesAPIErrors.INVALID_TAGS.description } , PostsRepliesAPIErrors.INVALID_TAGS.status_code
            if len(list(data.get("tags")))==0:
                return {"msg": PostsRepliesAPIErrors.INVALID_TAGS.description } , PostsRepliesAPIErrors.INVALID_TAGS.status_code
            
            
            if (data.get("description")):
                post_obj.description=data.get("description")
            if (data.get("tags")):
                post_obj.tags=data.get("tags")
           
            db.session.commit()
            return {"msg":"Post edited successfully"}
            

        except Exception as e:
            print(e)
            return {"msg" : PostsRepliesAPIErrors.INTERNAL_ERROR.description } , PostsRepliesAPIErrors.INTERNAL_ERROR.status_code
        


    @jwt_required()
    def delete(self,postid):
        try:
            curr_user = get_jwt_identity()
            post_obj = Posts.query.filter_by(id=postid).first()

            if curr_user.get("id")!=post_obj.user_id:
                if curr_user.get("role")!="admin":
                    if curr_user.get("role")!="super admin":
                        return {"msg" : PostsRepliesAPIErrors.INVALID_EDIT.description } , PostsRepliesAPIErrors.INVALID_EDIT.status_code
            if not post_obj:
                return {"msg": PostsRepliesAPIErrors.POSTID_INVALID.description}, PostsRepliesAPIErrors.DESCRITPTION_REQUIRED.status_code
            
            db.session.delete(post_obj)
            db.session.commit()
            return {"msg":"Deleted successfully"}
            
        except Exception as e:
            print(e)
            return {"msg" : PostsRepliesAPIErrors.INTERNAL_ERROR.description } , PostsRepliesAPIErrors.INTERNAL_ERROR.status_code
        