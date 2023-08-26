from functools import wraps
from flask_jwt_extended import get_jwt_identity
from application.models import User

def roles_accepted(roles):
    """
    Decorator to check if the current user has one of the accepted roles.

    This decorator checks if the current user has one of the specified roles
    to access the decorated API endpoint. If the user's role is not in the list
    of accepted roles, it returns a 401 Unauthorized status code.

    Parameters:
        roles (list): List of accepted roles for the API endpoint.

    Returns:
        function: Decorated function that checks the user's role before calling
        the original API endpoint function.
    """
    
    def decorator(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            
            user_identity = get_jwt_identity()
            user_id = user_identity.get("id")
            
            current_user = User.query.filter_by(id=user_id).first()

            if current_user.role not in roles:
                return {"msg" : "Unauthorized"} , 401
            
            return original_function(*args, **kwargs)
        return wrapper
    return decorator