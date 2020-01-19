from flask_restplus import Namespace, Resource, abort
from backend.models import db
from backend.models.couple_present import CouplePresent
from backend.models.user.wrappers import login_required, requires_access_level
from backend.constants import AL_FLOOR_MANAGER


api = Namespace("floor_manager", description="Floor Manager")


@api.route("/<int:couple_present_id>")
class FloorManagerAPISpecific(Resource):

    @api.doc("couple_present")
    @api.param("present", "Mark couple present/absent")
    @login_required
    @requires_access_level([AL_FLOOR_MANAGER])
    def patch(self, couple_present_id):
        """Mark couple present"""
        cp = CouplePresent.query.get(couple_present_id)
        if cp is not None:
            cp.present = api.payload["present"]
            cp.mark_in_next_heat(api.payload["present"])
            db.session.commit()
            return cp.json()
        abort(404, "Unknown couple_present_id")
