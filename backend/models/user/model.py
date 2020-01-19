from backend.models.base import db, TrackModifications, login, TABLE_USER
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER, AL_FLOOR_MANAGER, AL_ADJUDICATOR, AL_PRESENTER, SECONDS_DAY
import jwt
from time import time
from .util import get_token_from_request


class Anonymous(AnonymousUserMixin):

    @staticmethod
    def is_tournament_office_manager():
        return False

    @staticmethod
    def is_floor_manager():
        return False

    @staticmethod
    def is_adjudicator():
        return False

    @staticmethod
    def is_presenter():
        return False


@login.request_loader
def load_user(req):
    data = get_token_from_request(req)
    if data is not None:
        try:
            user_id = data["id"]
            reset_index = data["reset_index"]
            return User.query.filter(User.user_id == user_id, User.reset_index == reset_index).first()
        except (jwt.exceptions.InvalidTokenError, AttributeError, KeyError):
            return None
    return None


@login.user_loader
def load_user(user_id):
    try:
        user_id = user_id.split("-")
        return User.query.filter(User.user_id == user_id[0], User.reset_index == user_id[1]).first()
    except AttributeError:
        return None


class User(UserMixin, db.Model, TrackModifications):
    __tablename__ = TABLE_USER
    user_id = db.Column(db.Integer, primary_key=True)
    reset_index = db.Column(db.Integer, nullable=False, default=0)
    username = db.Column(db.String(64), unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer, index=True, nullable=False)

    def get_id(self):
        return f"{self.user_id}-{self.reset_index}"

    def __repr__(self):
        return f"{self.username}"

    def get_username(self):
        return self.adjudicator.name if self.is_adjudicator() else self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_tournament_office_manager(self):
        return self.access == AL_TOURNAMENT_OFFICE_MANAGER

    def is_floor_manager(self):
        return self.access == AL_FLOOR_MANAGER

    def is_adjudicator(self):
        return self.access == AL_ADJUDICATOR

    def is_presenter(self):
        return self.access == AL_PRESENTER

    def get_auth_token(self, expires_in=SECONDS_DAY):
        return jwt.encode({
            "id": self.user_id,
            "reset_index": self.reset_index,
            "username": self.get_username(),
            "tag": self.adjudicator.tag if self.is_adjudicator() else "",
            "access": self.access,
            "iat": time(),
            "exp": time() + expires_in,
            }, current_app.config["SECRET_KEY"],  algorithm="HS256").decode("utf-8")

    def json(self):
        data = {
            "id": self.user_id,
            "username": self.username,
        }
        if self.is_adjudicator():
            data.update({
                "username": self.adjudicator.name,
                "tag": self.adjudicator.tag,
            })
        return data
