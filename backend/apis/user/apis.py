from flask_restplus import Namespace, Resource
from backend.models.user import User
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level

api = Namespace("user", description="Users")


@api.route("/")
class UserAPI(Resource):
    @api.doc("list_users")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """List all users"""
        return [u.json() for u in User.query.all()]


@api.route("/<int:user_id>")
@api.param("user_id", "User id")
@api.response(404, "User not found")
class UserAPISpecific(Resource):
    @api.doc("get_user")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, user_id):
        """Fetch a specific user"""
        return User.get_or_404(user_id).json()
