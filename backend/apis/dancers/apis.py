from flask_restplus import Namespace, Resource, abort
from backend.models.dancer import Dancer
from backend.models import db
from backend.models.competition import Competition
from backend.models.event import Event
from backend.constants import LEAD, FOLLOW, AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level


BOTH = "both"


api = Namespace("dancers", description="Dancers")


def dancers():
    return [d.json() for d in Dancer.query.order_by(Dancer.number, Dancer.role).all()]


@api.route("/")
class DancerAPI(Resource):

    @api.doc("dancers")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """All couples"""
        return dancers()

    @api.doc("post_dancers")
    @api.param("number", "Number")
    @api.param("name", "Name")
    @api.param("role", "Role")
    @api.param("team", "Team")
    @api.param("competitions", "List of competitions_ids")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new dancer"""
        dancer = Dancer()
        dancer.name = api.payload["name"]
        dancer.number = api.payload["number"]
        dancer.role = api.payload["role"]
        dancer.team = api.payload["team"]
        comps = Competition.query.filter(Competition.competition_id.in_(api.payload["competitions"])).all()
        dancer.set_competitions(comps)
        db.session.add(dancer)
        db.session.commit()
        event = Event.query.filter(Event.is_active.is_(True)).first()
        competitions = [c.json() for c in event.competitions_by_date()] if event is not None else []
        return {
            "dancers": dancers(),
            "competitions": competitions,
        }


@api.route("/<int:dancer_id>")
class DancerAPISpecific(Resource):

    @api.doc("get_dancers")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, dancer_id):
        """Specific couple"""
        dancer = Dancer.query.get(dancer_id)
        if dancer is not None:
            return dancer.dancer_json()
        abort(404, "Unknown dancer_id")

    @api.doc("patch_dancers")
    @api.param("number", "Number")
    @api.param("name", "Name")
    @api.param("role", "Role")
    @api.param("team", "Team")
    @api.param("competitions", "List of competitions_ids")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, dancer_id):
        """Update existing dancer"""
        dancer = Dancer.query.get(dancer_id)
        if dancer is not None:
            dancer.name = api.payload["name"]
            dancer.number = api.payload["number"]
            dancer.role = api.payload["role"]
            dancer.team = api.payload["team"]
            comps = Competition.query.filter(Competition.competition_id.in_(api.payload["competitions"])).all()
            dancer.set_competitions(comps)
            db.session.commit()
            event = Event.query.filter(Event.is_active.is_(True)).first()
            competitions = [c.json() for c in event.competitions_by_date()] if event is not None else []
            return {
                "dancer": dancer.json(),
                "competitions": competitions,
            }
        abort(404, "Unknown dancer_id")

    @api.doc("delete_dancers")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, dancer_id):
        """Delete dancer"""
        dancer = Dancer.query.get(dancer_id)
        if dancer is not None:
            if dancer.deletable():
                db.session.delete(dancer)
                db.session.commit()
                return dancer_id
            abort(400, "Dancer cannot be deleted.")
        abort(404, "Unknown dancer_id")


@api.route("/csv")
class DancerAPICSV(Resource):

    @api.doc("post_dancers")
    @api.param("csv", "List of csv strings")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new dancers from list of csv strings"""
        import_list = api.payload["csv"].split("\n")
        counter = 0
        for import_string in import_list:
            data = import_string.split(",")
            if len(data) == 4:
                number, name, team, role = [d.strip() for d in data]
                role = role.lower()
                roles = []
                lead = LEAD.lower()
                follow = FOLLOW.lower()
                if role == lead or role == BOTH:
                    roles.append(LEAD)
                if role == follow or role == BOTH:
                    roles.append(FOLLOW)
                for r in roles:
                    check_dancer = Dancer.query.filter(Dancer.number == number, Dancer.role == r).first()
                    if check_dancer is None:
                        dancer = Dancer()
                        dancer.number = number
                        dancer.name = name
                        dancer.team = team
                        dancer.role = r
                        db.session.add(dancer)
                        counter += 1
        db.session.commit()
        return {
            "dancers": dancers(),
            "added": counter,
        }
