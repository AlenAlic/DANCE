from flask_restplus import Namespace, Resource, abort
from .functions import create_adjudicators, create_couples
from backend.constants import OK
from backend.models import db
from backend.models.couple import Couple
from backend.models.adjudicator import Adjudicator
from backend.models.round import Round
from backend.models.final_placing import FinalPlacing
import random
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level


api = Namespace("debug", description="Endpoints useful for testing")


@api.route("/test_data")
class DebugAPITestData(Resource):
    @api.doc("test_data")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Populate the system with test data"""
        if len(Adjudicator.query.all()) == 0:
            create_adjudicators()
        if len(Couple.query.all()) == 0:
            create_couples()
        return OK


@api.route("/adjudicate_round/<int:round_id>")
@api.param("round_id", "Round id")
class DebugAPIAdjudicateRound(Resource):

    @api.doc("adjudicate_round")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, round_id):
        """Fill the round with random marks/placings"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.is_final():
                for dance in r.dances:
                    for adj in r.competition.sorted_adjudicators():
                        placings = FinalPlacing.query.filter(FinalPlacing.adjudicator == adj,
                                                             FinalPlacing.dance == dance, FinalPlacing.round == r).all()
                        placings = [p for p in placings]
                        random.shuffle(placings)
                        for idx, p in enumerate(placings, 1):
                            p.final_placing = idx
                db.session.commit()
            else:
                for dance in r.dances:
                    for adj in r.competition.sorted_adjudicators():
                        marks = r.ordered_marks(dance_id=dance.dance_id, adjudicator=adj)
                        random.shuffle(marks)
                        for mark in marks[0:random.randrange(r.min_marks, r.max_marks + 1)]:
                            mark.mark = True
                db.session.commit()
            return OK
        abort(404, "Unknown round_id")

    @api.doc("clear_adjudicate_round")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, round_id):
        """Clear the round marks"""
        r = Round.query.get(round_id)
        if r is not None:
            if not r.is_final():
                marks = [mark for heat in r.heats for mark in heat.marks]
                for mark in marks:
                    mark.mark = False
                db.session.commit()
            return OK
        abort(404, "Unknown round_id")
