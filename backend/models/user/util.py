from flask import current_app
import jwt
from jwt import ExpiredSignatureError
from contextlib import suppress


def get_token_from_request(req):
    token = req.headers.get("Authorization")
    if token is not None:
        return decode_token(token.replace("Bearer ", ""))
    return None


def decode_token(token):
    with suppress(ExpiredSignatureError):
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    return None
