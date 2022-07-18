from flask import redirect, session, g
from functools import wraps


def auth_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def test_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # g mean App Context Global
        # Passing Data From Controlling Middleware to Another Function Call
        something = None
        if (something == True):
            g.somedata = []
        return func(*args, **kwargs)
    return decorated_function
