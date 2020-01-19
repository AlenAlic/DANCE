from flask_restplus import Namespace, Resource, abort
from backend.models.adjudicator import Adjudicator
from backend.models import db
from backend.models.user import User
from backend.constants import AL_ADJUDICATOR, AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level


api = Namespace("adjudicators", description="Adjudicators")


def adjudicators():
    return [a.json() for a in Adjudicator.query.order_by(Adjudicator.name).all()]


@api.route("/")
class AdjudicatorsAPI(Resource):

    @api.doc("adjudicators")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """All adjudicators"""
        return adjudicators()

    @api.doc("post_adjudicators")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @api.param("password", "Password")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new dancer"""
        u = User()
        u.username = api.payload["tag"]
        u.set_password(api.payload["password"])
        u.is_active = True
        u.access = AL_ADJUDICATOR
        adj = Adjudicator()
        adj.name = api.payload["name"]
        adj.tag = api.payload["tag"]
        adj.user = u
        db.session.add(adj)
        db.session.commit()
        return adjudicators()


@api.route("/<int:adjudicator_id>")
class AdjudicatorsAPISpecific(Resource):

    @api.doc("get_adjudicators")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, adjudicator_id):
        """Specific adjudicator"""
        adjudicator = Adjudicator.query.get(adjudicator_id)
        if adjudicator is not None:
            return adjudicator.json()
        abort(404, "Unknown adjudicator_id")

    @api.doc("patch_adjudicators")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @api.param("password", "Password")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, adjudicator_id):
        """Update existing adjudicator"""
        adjudicator = Adjudicator.query.get(adjudicator_id)
        if adjudicator is not None:
            adjudicator.name = api.payload["name"]
            adjudicator.tag = api.payload["tag"]
            adjudicator.user.username = api.payload["tag"]
            if api.payload["password"] is not None:
                adjudicator.user.set_password(api.payload["password"])
            return adjudicator.json()
        abort(404, "Unknown dancer_id")

    @api.doc("delete_adjudicators")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, adjudicator_id):
        """Delete adjudicator"""
        adjudicator = Adjudicator.query.get(adjudicator_id)
        if adjudicator is not None:
            if adjudicator.deletable():
                db.session.delete(adjudicator)
                db.session.commit()
                return adjudicators()
            abort(400, "Adjudicator cannot be deleted.")
        abort(404, "Unknown adjudicator_id")
