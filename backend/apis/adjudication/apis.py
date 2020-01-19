from flask_login import current_user
from flask_restplus import Namespace, Resource, abort
from backend.models.round import Round
from backend.models.dance import Dance
from backend.models.adjudicator_competition_assignment import AdjudicatorCompetitionAssignment
from backend.models.mark import Mark
from backend.models.dance_active import DanceActive
from backend.models import db
from backend.models.user.wrappers import login_required, requires_adjudicator_access_level


api = Namespace("adjudication", description="Adjudication")


def adjudicator(r):
    return AdjudicatorCompetitionAssignment.query\
        .filter(AdjudicatorCompetitionAssignment.competition_id == r.competition_id,
                AdjudicatorCompetitionAssignment.adjudicator == current_user.adjudicator).first()


def adjudication_mapping(r, adj, dance):
    return {
        h.heat_number(): [
            m.json() for m in h.ordered_marks(adjudicator(r).adjudicator)
        ] for h in r.heats if h.dance_id == dance.dance_id and (h.floor == adj.floor or h.floor is None)
    }


def adjudication_data(r, d):
    dance_active = DanceActive.query.filter(DanceActive.round == r, DanceActive.dance == d).first()
    data = {
        "round": r.json(),
        "dance": dance_active.json(),
        "adjudicator": adjudicator(r).json(),
        "next_dance": r.next_dance_json(d),
        "previous_dance": r.previous_dance_json(d),
        "marks": adjudication_mapping(r, adjudicator(r), d),
        "placings": [p.json() for p in r.ordered_final_placings(dance_id=d.dance_id,
                                                                adjudicator=adjudicator(r).adjudicator)]
    }
    return data


@api.route("/round/<int:round_id>/dance/<int:dance_id>")
@api.param("round_id", "Round id")
@api.param("dance_id", "Dance id")
class AdjudicationAPI(Resource):

    @api.doc("adjudicators")
    @login_required
    @requires_adjudicator_access_level
    def get(self, round_id, dance_id):
        """Adjudication data"""
        r = Round.query.get(round_id)
        if r is not None:
            d = Dance.query.get(dance_id)
            if d is not None:
                current_user.adjudicator.round = round_id
                current_user.adjudicator.dance = dance_id
                db.session.commit()
                return adjudication_data(r, d)
            abort(404, "Unknown dance_id")
        abort(404, "Unknown round_id")


@api.route("/dashboard")
class AdjudicationAPIDashboard(Resource):

    @api.doc("adjudicators")
    @login_required
    @requires_adjudicator_access_level
    def get(self):
        """All all competitions of an adjudicator"""
        current_user.adjudicator.round = 0
        current_user.adjudicator.dance = 0
        db.session.commit()
        return current_user.adjudicator.grouped_competitions()


@api.route("/mark/<int:mark_id>/mark")
@api.param("mark_id", "Mark id")
class AdjudicationAPIMark(Resource):

    @api.doc("patch_adjudication_mark")
    @api.param("mark", "Mark")
    @login_required
    @requires_adjudicator_access_level
    def patch(self, mark_id):
        """Mark a couple"""
        mark = Mark.query.get(mark_id)
        if mark is not None:
            if mark.heat.round.is_dance_active(mark.heat.dance):
                mark.mark = api.payload["mark"]
                mark.notes = 0
                db.session.commit()
                return adjudication_mapping(mark.heat.round, adjudicator(mark.heat.round), mark.heat.dance)
                # return mark.json()
            return adjudication_data(mark.heat.round, mark.heat.dance), 400
        abort(404, "Unknown mark_id")


@api.route("/mark/<int:mark_id>/notes")
@api.param("mark_id", "Mark id")
class AdjudicationAPINote(Resource):

    @api.doc("patch_adjudication_mark")
    @api.param("notes", "Mark")
    @login_required
    @requires_adjudicator_access_level
    def patch(self, mark_id):
        """Note a couple"""
        mark = Mark.query.get(mark_id)
        if mark is not None:
            if mark.heat.round.is_dance_active(mark.heat.dance):
                if not mark.mark:
                    mark.notes = api.payload["notes"] % 4
                else:
                    mark.notes = 0
                db.session.commit()
                return adjudication_mapping(mark.heat.round, adjudicator(mark.heat.round), mark.heat.dance)
                # return mark.json()
            return adjudication_data(mark.heat.round, mark.heat.dance), 400
        abort(404, "Unknown mark_id")


@api.route("/round/<int:round_id>/dance/<int:dance_id>/placings")
@api.param("round_id", "Round id")
class AdjudicatorAPIFinalPlacings(Resource):

    @api.doc("patch_adjudication_mark")
    @api.param("placings", "List of FinalPlacing objects")
    @login_required
    @requires_adjudicator_access_level
    def patch(self, round_id, dance_id):
        """Set final placings"""
        r = Round.query.get(round_id)
        if r is not None:
            d = Dance.query.get(dance_id)
            if d is not None:
                if r.is_dance_active(d):
                    placings = {p["final_placing_id"]: p["final_placing"] for p in api.payload["placings"]}
                    for placing in r.ordered_final_placings(dance_id=dance_id,
                                                            adjudicator=adjudicator(r).adjudicator):
                        placing.final_placing = placings[placing.final_placing_id]
                    db.session.commit()
                    return [p.json() for p in r.ordered_final_placings(dance_id=d.dance_id,
                                                                       adjudicator=adjudicator(r).adjudicator)]
                return adjudication_data(r, d), 400
            abort(404, "Unknown dance_id")
        abort(404, "Unknown round_id")
