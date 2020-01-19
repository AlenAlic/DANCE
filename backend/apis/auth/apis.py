from flask_restplus import Namespace, Resource, abort
from .functions import check_password_requirements
from flask import jsonify, request
from flask_login import current_user, logout_user
from backend.models import db
from backend.models.user import User
from backend.models.user.util import get_token_from_request
from backend.constants import OK, SECONDS_MONTH, SECONDS_DAY
from backend.models.user.wrappers import login_required


api = Namespace("auth", description="Authentication")


@api.route("/login")
class AuthAPILogin(Resource):
    @api.doc("login", security=None)
    @api.param("email", "Email/Username")
    @api.param("password", "Password")
    @api.param("remember_me", "Remember me flag (longer duration token)")
    def post(self):
        """Get authentication token"""
        u = User.query.filter(User.username == api.payload["email"]).first()
        if u is None or not u.check_password(api.payload["password"]):
            abort(401, "Password incorrect")
        elif u.is_active:
            return jsonify(u.get_auth_token(expires_in=SECONDS_MONTH if api.payload["remember_me"] else SECONDS_DAY))
        return abort(403, "Account inactive")


@api.route("/renew")
class AuthAPIRenew(Resource):
    @api.doc("renew")
    @login_required
    def get(self):
        """Renew authentication token"""
        data = get_token_from_request(request)
        if data is not None:
            return jsonify(current_user.get_auth_token(expires_in=int(data["exp"] - data["iat"])))
        return abort(401, "Token expired")


@api.route("/logout")
class AuthAPILogout(Resource):
    @api.doc("logout")
    @login_required
    def delete(self):
        """Log out"""
        logout_user()
        return ""


@api.route("/password/change/<int:user_id>")
class AuthAPIChangePassword(Resource):
    @api.doc("chance_password")
    @login_required
    def patch(self, user_id):
        """Change password"""
        u = User.query.filter(User.user_id == user_id).first()
        if u.check_password(api.payload["current_password"]):
            if check_password_requirements(api.payload["new_password"], api.payload["repeat_password"]) \
                    and api.payload["new_password"] != api.payload["current_password"]:
                u.set_password(api.payload["new_password"], increment=False)
                db.session.commit()
                return OK
            else:
                return abort(400, "Password requirements not met")
        return abort(401, "Current password incorrect")
