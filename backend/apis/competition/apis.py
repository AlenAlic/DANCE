from flask_restplus import Namespace, Resource, abort
from backend.util import datetime_python
from backend.models import db, active_event
from backend.models.event import Event
from backend.models.competition import Competition
from backend.models.competition.enums import CompetitionMode
from backend.models.adjudicator import Adjudicator
from backend.models.couple import Couple
from backend.models.dancer import Dancer
from backend.models.dance import Dance
from backend.models.dance_active import DanceActive
from backend.models.round import Round
from backend.models.round.enums import RoundType
from backend.apis.adjudicators import adjudicators
from backend.models.user.wrappers import login_required, requires_access_level
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER, AL_FLOOR_MANAGER, AL_PRESENTER


api = Namespace("competition", description="Competitions")


def competitions():
    e = active_event()
    if e is not None:
        return active_event().competitions_by_date()
    return []


@api.route("/")
class CompetitionAPI(Resource):

    @api.doc("list_competitions")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """List all competitions of the active Event"""
        return [c.json() for c in competitions()]

    @api.doc("create_competition")
    @api.param("discipline", "Discipline of the competition.")
    @api.param("dancing_class", "Discipline of the competition.")
    @api.param("floors", "Max number of floors the competition will be held on.")
    @api.param("date", "Date of the competition.")
    @api.param("mode", "Mode of the competition.")
    @api.param("qualification", "Qualification round of the competition.")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create a new competition"""
        event = Event.query.filter(Event.is_active.is_(True)).first()
        c = Competition()
        c.discipline_id = api.payload["discipline"]
        c.dancing_class_id = api.payload["dancing_class"]
        c.floors = api.payload["floors"]
        c.when = datetime_python(api.payload["date"])
        c.mode = api.payload["mode"]
        c.qualification_id = api.payload["qualification"]
        c.event = event
        db.session.add(c)
        db.session.commit()
        return [c.json() for c in event.competitions_by_date()]


@api.route("/<int:competition_id>")
@api.param("competition_id", "Competition id")
@api.response(404, "Competition not found")
class CompetitionAPISpecific(Resource):

    @api.doc("get_competition")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, competition_id):
        """Fetch a specific Competition"""
        c = Competition.query.get(competition_id)
        if c is not None:
            return c.json()
        abort(404, "Unknown competition_id")

    @api.doc("get_competition")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, competition_id):
        """Update a Competition"""
        c = Competition.query.get(competition_id)
        if c is None:
            abort(404, "Unknown competition_id")
        c.discipline_id = api.payload["discipline"]
        c.dancing_class_id = api.payload["dancing_class"]
        c.floors = api.payload["floors"]
        c.when = datetime_python(api.payload["date"])
        c.mode = api.payload["mode"]
        c.qualification_id = api.payload["qualification"]
        c.adjudicators = Adjudicator.query.filter(Adjudicator.adjudicator_id.in_(api.payload["adjudicators"])).all()
        c.update_adjudicator_assignments()
        if c.mode == CompetitionMode.single_partner.name:
            c.couples = Couple.query.filter(Couple.couple_id.in_(api.payload["couples"])).all()
            c.leads = []
            c.follows = []
        else:
            c.couples = []
            c.leads = Dancer.query.filter(Dancer.dancer_id.in_(api.payload["leads"])).all()
            c.follows = Dancer.query.filter(Dancer.dancer_id.in_(api.payload["follows"])).all()
        db.session.commit()
        return {
            "competition": c.json(),
            "adjudicators": adjudicators(),
        }

    @api.doc("delete_competition")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, competition_id):
        """Fetch a specific Competition"""
        c = Competition.query.get(competition_id)
        if c is not None:
            db.session.delete(c)
            db.session.commit()
            return competition_id
        abort(404, "Unknown competition_id")


@api.route("/<int:competition_id>/round")
@api.param("competition_id", "Competition id")
@api.response(404, "Competition not found")
class CompetitionAPIRound(Resource):

    @api.doc("create_round")
    @api.param("type", "Round type.")
    @api.param("heats", "Number of heats for the round.")
    @api.param("floors", "Number of floors the round will be danced on.")
    @api.param("min_marks", "Min target marks.")
    @api.param("max_marks", "Max target marks.")
    @api.param("dances", "List of dance ids.")
    @api.param("different_heats", "Indicates if couples should dance each dance in the same heat.")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, competition_id):
        """Create the first round for the competition"""
        c = Competition.query.get(competition_id)
        if c is not None:
            r = Round()
            r.type = api.payload["type"]
            r.set_marks(api.payload["min_marks"], api.payload["max_marks"])
            r.is_active = False
            r.competition = c
            r.dances = Dance.query.filter(Dance.dance_id.in_(api.payload["dances"])).all()
            for dance in r.dances:
                da = DanceActive()
                da.round = r
                da.dance = dance
                r.dance_active.append(da)
            r.couples = c.generate_couples()
            if api.payload["type"] == RoundType.final.name:
                r.create_final()
            else:
                r.create_heats(int(api.payload["heats"]), floors=int(api.payload["floors"]),
                               different_heats=api.payload["different_heats"])
            db.session.commit()
            return c.json()
        abort(404, "Unknown competition_id")


@api.route("/<int:competition_id>/floor_assignments")
@api.param("competition_id", "Competition id")
@api.response(404, "Competition not found")
class CompetitionAPIFloorAssignments(Resource):

    @api.doc("floor_assignments")
    @api.param("floor_assignments", "Floor assignments")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, competition_id):
        """Assign adjudicators to a floor"""
        c = Competition.query.get(competition_id)
        if c is not None:
            for a in c.adjudicator_assignments:
                a.floor = api.payload["floor_assignments"][str(a.adjudicator_competition_assignment_id)]
            db.session.commit()
            return c.json()
        abort(404, "Unknown competition_id")


@api.route("/<int:competition_id>/role_assignments")
@api.param("competition_id", "Competition id")
@api.response(404, "Competition not found")
class CompetitionAPIRoleAssignments(Resource):

    @api.doc("role_assignments")
    @api.param("role_assignments", "Role assignments")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, competition_id):
        """Assign adjudicators to a adjudicate a specific role"""
        c = Competition.query.get(competition_id)
        if c is not None:
            for a in c.adjudicator_assignments:
                a.assignment = api.payload["role_assignments"][str(a.adjudicator_competition_assignment_id)]
            db.session.commit()
            return c.json()
        abort(404, "Unknown competition_id")


@api.route("/starting_lists")
class CompetitionAPIStartingLists(Resource):
    @api.doc("starting_lists", security=None)
    def get(self):
        """List all competitions for the starting lists"""
        return [c.starting_lists_json() for c in competitions() if c.show_starting_list()]


@api.route("/starting_lists/<int:competition_id>")
@api.param("competition_id", "Competition id")
class CompetitionAPIStartingListsSpecific(Resource):
    @api.doc("starting_lists_competition", security=None)
    def get(self, competition_id):
        c = Competition.query.get(competition_id)
        if c is not None:
            if c.starting_list_visible():
                return c.starting_list_data()
            return c.starting_lists_json(), 400
        abort(404, "Unknown competition_id")


@api.route("/heat_lists")
class HeatListsAPI(Resource):
    @api.doc("heat_lists", security=None)
    def get(self):
        """List all competitions for the heat lists"""
        return [c.heat_lists_json() for c in competitions() if c.show_starting_list()]


@api.route("/heat_lists/<int:competition_id>")
@api.param("competition_id", "Competition id")
class CompetitionAPIHeatListsSpecific(Resource):
    @api.doc("heat_lists_competition", security=None)
    def get(self, competition_id):
        c = Competition.query.get(competition_id)
        if c is not None:
            r = c.last_round_with_heat_list_published()
            if r is not None:
                return {
                    "round": r.json(),
                    "data": {
                        "competitors": r.competitors(),
                        "heat_mapping": r.couple_dance_heat_mapping(),
                        "partner_mapping": r.lead_follow_mapping() if r.competition.is_change_per_dance() else {}
                    },
                }
            return c.publish_json(), 400
        abort(404, "Unknown competition_id")


@api.route("/results")
class CompetitionAPIResults(Resource):
    @api.doc("get_competitions_results", security=None)
    def get(self):
        """List all competitions of the active Event that can have results published"""
        return [c.publish_json() for c in competitions() if c.show_result_list()]

    @api.doc("patch_competitions_results")
    @api.param("competitions", "List of competition_ids that should have their results published")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self):
        """Publish the results of these"""
        event = active_event()
        Competition.query.filter(Competition.event == event)\
            .update({Competition.results_published: False}, synchronize_session="fetch")
        comps = Competition.query.filter(Competition.competition_id.in_(api.payload["competitions"])).all()
        for c in comps:
            if c.first_round() and c.first_round().is_completed():
                c.results_published = True
        for c in active_event().competitions:
            if not c.results_published:
                c.results_string = None
        db.session.commit()
        return [c.publish_json() for c in event.competitions_by_date() if not c.test]


@api.route("/results/<int:competition_id>")
@api.param("competition_id", "Competition id")
class CompetitionAPIResultsSpecific(Resource):
    @api.doc("results_competition", security=None)
    def get(self, competition_id):
        c = Competition.query.get(competition_id)
        if c is not None:
            if c.results_published:
                if not c.results_string:
                    data = c.results()
                    c.results_string = data
                    db.session.commit()
                return c.results_string
            return c.publish_json(), 400
        abort(404, "Unknown competition_id")


@api.route("/floor_manager")
class CompetitionAPIFloorManagerLists(Resource):
    @api.doc("floor_manager")
    @login_required
    @requires_access_level([AL_FLOOR_MANAGER])
    def get(self):
        """List all competitions available for the floor manager"""
        return [c.publish_json() for c in competitions() if c.show_starting_list()]


@api.route("/floor_manager/<int:competition_id>")
@api.param("competition_id", "Competition id")
class CompetitionAPIFloorManagementFirstDance(Resource):

    @api.doc("get_floor_manager")
    @login_required
    @requires_access_level([AL_FLOOR_MANAGER])
    def get(self, competition_id):
        """Get floor management data for the first dance"""
        c = Competition.query.get(competition_id)
        if c is not None:
            r = c.last_round()
            if r is not None:
                if r.heat_list_published and not r.is_final():
                    return {
                        "round": r.json(),
                        "data": r.floor_management_data(r.first_dance().dance_id),
                    }
            return c.publish_json(), 400
        abort(404, "Unknown competition_id")


@api.route("/floor_manager/<int:competition_id>/dance/<int:dance_id>")
@api.param("competition_id", "Competition id")
@api.param("dance_id", "Dance id")
class CompetitionAPIFloorManagementSpecificDance(Resource):

    @api.doc("get_floor_manager")
    @login_required
    @requires_access_level([AL_FLOOR_MANAGER])
    def get(self, competition_id, dance_id):
        """Get floor management data for a specific dance"""
        c = Competition.query.get(competition_id)
        if c is not None:
            r = c.last_round()
            if r is not None:
                if r.heat_list_published and not r.is_final():
                    d = Dance.query.get(dance_id)
                    if d in r.dances:
                        return r.floor_management_data(d.dance_id)
                    abort(400, "Dance not in round")
                abort(400, "Heat list not published")
            abort(400, "No last round")
        abort(404, "Unknown competition_id")


@api.route("/presenter")
class CompetitionAPIPresenter(Resource):
    @api.doc("presenter")
    @login_required
    @requires_access_level([AL_PRESENTER])
    def get(self):
        """List all competitions for the results"""
        return [c.publish_json() for c in competitions() if c.show_starting_list()]


@api.route("/presenter/<int:competition_id>")
@api.param("competition_id", "Competition id")
class CompetitionAPIPresenterCompetition(Resource):

    @api.doc("get_presenter_rounds")
    @login_required
    @requires_access_level([AL_PRESENTER])
    def get(self, competition_id):
        """Get presenter data for a specific competition"""
        c = Competition.query.get(competition_id)
        if c is not None:
            return c.presenter_rounds()
        abort(404, "Unknown competition_id")
