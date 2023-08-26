class ErrorCodes:
    status_code = None
    description = None

    def __init__(self,status_code, description):
        self.status_code = status_code
        self.description = description

class APIErrors:
    INTERNAL_ERROR = ErrorCodes(500,"Internal Server Error")

class AuthenticationAPIErrors(APIErrors):
    COMPULSORY_EMAIL = ErrorCodes(400,"Email is compulsory")
    USER_EXIST = ErrorCodes(409,"User already exists")
    PASSWORD_NOT_MATCH = ErrorCodes(400,"Password and Confirm Passwords must match")
    LEVEL_NOT_ACCEPTED = ErrorCodes(400,"This level is not accepted")
    COMPULSORY_NAME = ErrorCodes(400,"Name is compulsory")
    COMPULSORY_USERNAME = ErrorCodes(400,"Username is compulsory")
    INVALID_USERNAME = ErrorCodes(400,"Username is invalid. It can contain only upper case characters, lower case characters, numbers and underscore. It's length must be between 3 and 12")
    COMPULSORY_PASSWORD = ErrorCodes(400,"Password and Confirm Password is compulsory")
    INVALID_DATA = ErrorCodes(403,"Invalid Credentials")
    USER_BLOCKED = ErrorCodes(403,"You have been blocked by the adminstrators")
    TOKEN_EXPIRED = ErrorCodes(401,"Pin Expired. Please select resend pin to receive a new one")
    INVALID_PIN = ErrorCodes(400,"Invalid Pin")
    USER_NOT_FOUND = ErrorCodes(404,"User not found")

class InterviewAPIErrors(APIErrors):
    COMPULSORY_COMPANY_NAME = ErrorCodes(400,"Company name is compulsory")
    COMPULSORY_JOB_ROLE = ErrorCodes(400,"Job Role is compulsory")
    COMPULSORY_JOB_TYPE = ErrorCodes(400,"Job Type is compulsory")
    INVALID_JOB_TYPE = ErrorCodes(400,"Invalid Job Type. It can be either 'Full Time' or 'Internship'")
    DESCRIPTION_REQUIRED = ErrorCodes(400,"Description is required to add an interview")
    INTERVIEW_ID_REQUIRED = ErrorCodes(400,"Interview Id is required to edit")
    INTERVIEW_NOT_FOUND = ErrorCodes(400,"Interview not found")

class QuestionAPIErrors(APIErrors):
    COMPULSORY_QUESTION_NAME = ErrorCodes(400,"Question name is compulsory")
    TAGS_REQUIRED = ErrorCodes(400,"Minimun 1 tag is required")
    INVALID_TAGS = ErrorCodes(400,"Tags must be a list")
    DESCRIPTION_REQUIRED = ErrorCodes(400,"Question Description is required")
    QUESTION_TYPE_REQUIRED = ErrorCodes(400,"Question type is required")
    INVALID_QUESTION_TYPE = ErrorCodes(400,"Invalid Question type. It must be one of ['MCQ','MSQ','NAT','Coding']")
    OPTIONS_REQUIRED = ErrorCodes(400,"Minimum 4 options are required. Keys must be 1,2,3 and 4")
    INVALID_OPTIONS = ErrorCodes(400,"Options must have key value pairs")
    INVALID_ANSWER = ErrorCodes(400,"Answers must be a list of options(for MCQ and MSQ) or valid answers for NAT")
    ANSWER_REQUIRED = ErrorCodes(400,"Minimum 1 valid answer is required")
    QUESTION_EXISTS = ErrorCodes(400,"Question with this name already exists")
    QUESTION_NOT_FOUND = ErrorCodes(400,"Question not found")
    QUESTION_ID_REQUIRED = ErrorCodes(400,"Question Id is required to edit")

class PracticeTestAPIErrors(APIErrors):
    PRACTICE_TEST_NAME_REQUIRED = ErrorCodes(400,"Practice test name is compulsory")
    TAGS_REQUIRED = ErrorCodes(400,"Minimun 1 tag is required")
    INVALID_TAGS = ErrorCodes(400,"Tags must be a list")
    QUESTION_IDS_REQUIRED = ErrorCodes(400,"Question ids are required")
    QUESTION_IDS_LENGTH = ErrorCodes(400,"Minimum 5 questions are required")
    QUESTION_IDS_INVALID = ErrorCodes(400,"Question ids must be a list")
    PRACTICE_TEST_EXISTS = ErrorCodes(400,"Practice test with this name already exists")
    PRACTICE_TEST_NOT_FOUND = ErrorCodes(400,"Practice test not found")
    QUESTION_NOT_FOUND = ErrorCodes(400,"Question not found")
    PRACTICE_TEST_ID_REQUIRED = ErrorCodes(400,"Practice test Id is required to edit")
    
class UsersAPIErrors(APIErrors):
    USER_NOT_EXIST = ErrorCodes(409,"User doesnot exists")

class PostsRepliesAPIErrors(APIErrors):
    DESCRITPTION_REQUIRED = ErrorCodes(400,"Description cannot be empty")
    INVALID_TAGS = ErrorCodes(400,"Tags must be a list")
    TAGS_REQUIRED = ErrorCodes(400,"Minimun 1 tag is required")
    POSTID_REQUIRED = ErrorCodes(400,"Post Id required")
    POSTID_INVALID = ErrorCodes(400,"Post not found")
    REPLYID_REQUIRED = ErrorCodes(400,"Reply Id required")
    REPLYID_INVALID = ErrorCodes(400,"Reply not found")
    INVALID_EDIT = ErrorCodes(400,"Cannot make changes to other user's post/reply")
    



    