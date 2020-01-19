from flask_restplus import Namespace, Resource, abort
from flask import jsonify, current_app
from backend.models import db, active_event
from backend.models.event_result import EventResult
from backend.models.competition.enums import CompetitionMode
from backend.models.round.enums import RoundType
from backend.models.adjudicator_competition_assignment.enums import AdjudicatorAssignmentEnum
from backend.models.dance import Dance
from backend.constants import OK, TOURNAMENT, XTDS, ODK, SOND, BEGINNERS, AMATEURS, PROFESSIONALS, MASTERS, CHAMPIONS, \
    CLOPEN_QUALIFICATION, CLOSED, OPEN_CLASS, BASE_DANCES, BONUS_DANCES, STANDARD, LATIN, \
    BASIC_STANDARD_DANCES, BASIC_LATIN_DANCES, SOND_JUNIOREN, SOND_SENIOREN, FLOOR_MAP, ALL_ROLES, \
    AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level
from backend.apis.event.functions import reset_db


api = Namespace("config", description="Config")


@api.route("/")
class ConfigAPI(Resource):
    @api.doc("config", security=None)
    def get(self):
        """Configuration for the site"""
        competitions = []
        if current_app.config.get(TOURNAMENT) == XTDS:
            competitions = [
                BEGINNERS,
                AMATEURS,
                PROFESSIONALS,
                MASTERS,
                CHAMPIONS,
                CLOPEN_QUALIFICATION,
                CLOSED,
                OPEN_CLASS,
            ]
        if current_app.config.get(TOURNAMENT) == ODK:
            competitions = [d["name"] for d in BASE_DANCES + BONUS_DANCES]
        if current_app.config.get(TOURNAMENT) == SOND:
            competitions = []
            competitions.extend([f"{STANDARD}&{c}" for c in SOND_JUNIOREN])
            competitions.extend([f"{STANDARD}&{c}" for c in SOND_SENIOREN])
            competitions.extend([f"{LATIN}&{c}" for c in SOND_JUNIOREN])
            competitions.extend([f"{LATIN}&{c}" for c in SOND_SENIOREN])
        return jsonify({
            "tournament": current_app.config.get(TOURNAMENT),
            "competitions": competitions,
            "competition_modes": [{"name": c.value, "value": c.name} for c in CompetitionMode],
            "round_types": [{"name": t.value, "value": t.name} for t in RoundType],
            "round_types_filter": {
                "1": [{"name": t.value, "value": t.name} for t in
                      [RoundType.qualification, RoundType.general_look, RoundType.first_round, RoundType.final]],
                "2": [{"name": t.value, "value": t.name} for t in [RoundType.qualification]],
                "3": [{"name": t.value, "value": t.name} for t in
                      [RoundType.re_dance, RoundType.intermediate_round, RoundType.eight_final,
                       RoundType.quarter_final, RoundType.semi_final, RoundType.final]],
                "4": [{"name": t.value, "value": t.name} for t in
                      [RoundType.intermediate_round, RoundType.eight_final, RoundType.quarter_final,
                       RoundType.semi_final, RoundType.final]],
                "5": [{"name": t.value, "value": t.name} for t in
                      [RoundType.eight_final, RoundType.quarter_final, RoundType.semi_final, RoundType.final]],
                "6": [{"name": t.value, "value": t.name} for t in
                      [RoundType.quarter_final, RoundType.semi_final, RoundType.final]],
                "7": [{"name": t.value, "value": t.name} for t in [RoundType.semi_final, RoundType.final]],
                "8": [{"name": t.value, "value": t.name} for t in [RoundType.final]],
                "9": [{"name": t.value, "value": t.name} for t in
                      [RoundType.qualification, RoundType.first_round, RoundType.final]],
            },
            "base_dances": {
                STANDARD: [d.json() for d
                           in Dance.query.filter(Dance.name.in_(BASIC_STANDARD_DANCES)).order_by(Dance.order).all()],
                LATIN: [d.json() for d
                        in Dance.query.filter(Dance.name.in_(BASIC_LATIN_DANCES)).order_by(Dance.order).all()]
            },
            "floors": [f for f in FLOOR_MAP.values()],
            "adjudication_assignments": [
                {"name": a.value, "value": a.name} for a in AdjudicatorAssignmentEnum
            ],
            "roles": ALL_ROLES
        })


@api.route("/reset")
class ConfigAPIReset(Resource):
    @api.doc("reset")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self):
        """Reset the database to the initial state"""
        reset_db()
        return OK


@api.route("/results")
class ConfigAPISaveResults(Resource):
    @api.doc("get_results")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """Get a list of the competitions that have results published"""
        e = active_event()
        if e is not None:
            comps = [c for c in e.competitions_by_date()]
            return {
                "saved": [c.publish_json() for c in comps if c.results_published],
                "ignored": [c.publish_json() for c in comps if not c.results_published],
            }
        abort(401, "No active event")

    @api.doc("save_results")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Save the event results"""
        e = active_event()
        if e is not None:
            for r in e.results:
                db.session.delete(r)
            for comp in [c for c in e.competitions if c.show_result_list() and c.results_published]:
                result = EventResult()
                result.save_results(comp)
            db.session.commit()
            return OK
        abort(401, "No active event")
