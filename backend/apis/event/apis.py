from flask import current_app, g
from flask_login import current_user, login_user, logout_user
from flask_restplus import Namespace, Resource, abort
from backend.models import db
from backend.models.event import Event
from backend.models.dance import Dance
from backend.models.discipline import Discipline
from backend.models.dancing_class import DancingClass
from backend.models.competition import Competition
from backend.models.user import User
from backend.constants import OK, TOURNAMENT, XTDS, ODK, SOND, AL_TOURNAMENT_OFFICE_MANAGER
from .functions import create_base_dances, create_disciplines, create_dancing_classes, create_second_base_dances, \
    generate_xtds_competitions, generate_odk_competitions, generate_sond_competitions
from datetime import datetime, date
from backend.models.adjudicator import Adjudicator
from backend.apis.adjudicators import adjudicators
from backend.apis.competition import competitions
from backend.models.user.wrappers import login_required, requires_access_level
from backend.models.event_result import EventResult


api = Namespace("event", description="Events")


@api.route("/")
class EventAPI(Resource):

    @api.doc("list_events", security=None)
    def get(self):
        """List all events"""
        return [e.json() for e in Event.query.all()]

    @api.doc("create_event")
    @api.param("name", "Event name")
    @api.param("date", "Date the event takes place")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create a new event"""
        e = Event()
        e.name = api.payload["name"]
        e.is_active = True
        e.date = date.fromtimestamp(datetime.strptime(api.payload["date"], "%Y-%m-%d").timestamp())
        db.session.add(e)
        db.session.commit()
        return OK


@api.route("/defaults")
class EventAPIDefaults(Resource):

    @api.doc("create_default_competitions")
    @api.param("competitions", "Competitions that will be held during the event")
    def post(self):
        """Create default dances, discipline, classes, and selected competitions"""
        create_base_dances()
        if current_app.config.get(TOURNAMENT) == XTDS or current_app.config.get(TOURNAMENT) == SOND:
            create_second_base_dances()
        create_dancing_classes()
        create_disciplines()
        g.event = Event.query.filter(Event.is_active.is_(True)).first()
        d = g.event.date
        start_time = datetime.utcfromtimestamp(datetime(d.year, d.month, d.day, 9).timestamp())
        if current_app.config.get(TOURNAMENT) == XTDS:
            generate_xtds_competitions(start_time, api.payload["competitions"])
        elif current_app.config.get(TOURNAMENT) == ODK:
            generate_odk_competitions(start_time, api.payload["competitions"])
        elif current_app.config.get(TOURNAMENT) == SOND:
            generate_sond_competitions(start_time, api.payload["competitions"])
        return {
            "dances": [d.json() for d in Dance.query.order_by(Dance.order).all()],
            "disciplines": [d.json() for d in Discipline.query.order_by(Discipline.name).all()],
            "classes": [d.json() for d in DancingClass.query.order_by(DancingClass.name).all()],
            "competitions": [c.json() for c in Competition.query.order_by(Competition.when).all()],
        }


@api.route("/<int:event_id>")
@api.param("event_id", "Event id")
@api.response(404, "Event not found")
class EventAPISpecific(Resource):

    @api.doc("get_event")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, event_id):
        """Fetch a specific Event"""
        e = Event.query.get(event_id)
        if e is not None:
            return e.json()
        abort(404, "Unknown event_id")


@api.route("/dashboard")
class EventAPIDashboard(Resource):

    @api.doc("get_dashboard")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """Get the dashboard data"""
        return {
            "users": [
                u.json() for u in User.query.filter(User.is_active.is_(True),
                                                    User != current_user).order_by(User.username).all()
            ]
        }

    @api.doc("switch user")
    @api.param("user_id", "User_id")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create a new event"""
        logout_user()
        user = User.query.get(api.payload["user_id"])
        # login_user(user)
        return user.get_auth_token()


@api.route("/assignments")
class EventAPIAssignments(Resource):

    @api.doc("switch user")
    @api.param("assignments", "List of strings {competition_id-adjudicator_id}")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self):
        """Assign adjudicators to competitions"""
        all_adjudicators = Adjudicator.query.order_by(Adjudicator.name).all()
        for comp in competitions():
            if comp.is_configurable():
                checks = [a for a in [f"{comp.competition_id}-{adj.adjudicator_id}"
                                      for adj in all_adjudicators] if a in api.payload["assignments"]]
                adj = [int(a) for a in [a.split('-')[1] for a in checks]]
                comp.adjudicators = Adjudicator.query.filter(Adjudicator.adjudicator_id.in_(adj)).all()
                comp.update_adjudicator_assignments()
        db.session.commit()
        return {
            "adjudicators": adjudicators(),
            "competitions": [c.json() for c in competitions()],
        }


@api.route("/<int:event_id>/results")
@api.param("event_id", "Event id")
@api.response(404, "Event not found")
class EventAPIResults(Resource):

    @api.doc("get_event_results_list")
    def get(self, event_id):
        """Fetch a specific Event results"""
        e = Event.query.get(event_id)
        if e is not None:
            if e.is_active:
                return [c.publish_json() for c in competitions() if c.show_result_list()]
            else:
                return {
                    "event": e.json(),
                    "results": [r.json() for r in e.sorted_results()],
                }
        abort(404, "Unknown event_id")


@api.route("/results/<int:event_result_id>")
@api.param("event_result_id", "Event result id")
@api.response(404, "Event result not found")
class EventAPIResults(Resource):

    @api.doc("get_event_result")
    def get(self, event_result_id):
        """Fetch a specific EventResult"""
        result = EventResult.query.get(event_result_id)
        if result is not None:
            return {
                "event": result.event.json(),
                "data": result.json(results=True),
            }
        abort(404, "Unknown event_result_id")
