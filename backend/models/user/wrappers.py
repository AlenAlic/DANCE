from functools import wraps
from flask_login import current_user
from backend.constants import UNAUTHORIZED, FORBIDDEN


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_anonymous:
            return UNAUTHORIZED
        return f(*args, **kwargs)
    return decorated_function


def requires_access_level(access_levels):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.access not in access_levels:
                return FORBIDDEN
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def requires_adjudicator_access_level(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_adjudicator():
            return FORBIDDEN
        return f(*args, **kwargs)
    return decorated_function
