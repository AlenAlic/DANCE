from flask_restplus import Namespace, Resource, abort
from backend.models import db
from backend.constants import OK
from backend.models.couple_present import CouplePresent
from backend.models.mark import Mark
from backend.models.dance import Dance
from backend.models.dance_active import DanceActive
from backend.models.round import Round
from backend.models.round.enums import RoundType
from backend.models.couple import Couple
from backend.models.heat import Heat
from backend.models.round_result import RoundResult
from backend.models.couple.functions import generate_new_couples_from_dancers
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER, AL_FLOOR_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level


api = Namespace("round", description="Rounds that are danced during a competition")


@api.route("/")
class RoundAPI(Resource):

    @api.doc("get_rounds")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """List all rounds"""
        return [r.json() for r in Round.query.all()]


@api.route("/<int:round_id>")
@api.param("round_id", "Specify the id of the Round.")
@api.response(200, "OK")
@api.response(404, "Round not found")
class RoundAPISpecific(Resource):

    @api.doc("get_round")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Fetch a specific Round"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.json()
        abort(404, "Unknown round_id")

    @api.doc("delete_round")
    @api.response(400, "Cannot delete round")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, round_id):
        """Delete a specific Round"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.deletable():
                c = r.competition
                db.session.delete(r)
                db.session.commit()
                return c.json()
            abort(400, "Cannot delete round")
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/progress")
@api.param("round_id", "Round id")
class RoundAPIProgress(Resource):

    @api.doc("get_progress")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get progress data"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.progress_data()
        abort(404, "Unknown round_id")

    @api.doc("post_progress")
    @api.param("type", "Round type.")
    @api.param("heats", "Number of heats for the round.")
    @api.param("floors", "Number of floors the round will be danced on.")
    @api.param("min_marks", "Min target marks.")
    @api.param("max_marks", "Max target marks.")
    @api.param("dances", "List of dance ids.")
    @api.param("different_heats", "Indicates if couples should dance each dance in the same heat.")
    @api.param("ids", "List of ids (couples or individual dancers) to place in the round.")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, round_id):
        """Create the next round"""
        previous_round = Round.query.get(round_id)
        if previous_round is not None:
            r = Round()
            r.type = api.payload["type"]
            r.set_marks(api.payload["min_marks"], api.payload["max_marks"])
            r.is_active = False
            r.competition = previous_round.competition
            r.dances = Dance.query.filter(Dance.dance_id.in_(api.payload["dances"])).all()
            for dance in r.dances:
                da = DanceActive()
                da.round = r
                da.dance = dance
                r.dance_active.append(da)
            results = RoundResult.query.filter(RoundResult.round_result_id.in_(api.payload["ids"])).all()
            if r.competition.is_change_per_dance():
                leads = [r.couple.lead for r in results if not r.follow]
                follows = [r.couple.follow for r in results if r.follow]
                r.couples = generate_new_couples_from_dancers(leads, follows)
            else:
                r.couples = [r.couple for r in results]
            if api.payload["type"] == RoundType.final.name:
                r.create_final()
            else:
                r.create_heats(int(api.payload["heats"]), floors=int(api.payload["floors"]),
                               different_heats=api.payload["different_heats"])
            db.session.commit()
            return previous_round.competition.json()
        abort(404, "Unknown competition_id")

    @api.doc("patch_progress")
    @api.param("type", "Round type.")
    @api.param("min_marks", "Min target marks.")
    @api.param("max_marks", "Max target marks.")
    @api.param("same_heats", "Flag to keep the heats the same, or shuffle up everything.")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id):
        """Create the next round after a general look"""
        previous_round = Round.query.get(round_id)
        if previous_round is not None:
            if api.payload["same_heats"] and api.payload["type"] != RoundType.final.name:
                r = previous_round
                r.type = api.payload["type"]
                r.set_marks(api.payload["min_marks"], api.payload["max_marks"])
                db.session.commit()
            else:
                r = Round()
                r.type = api.payload["type"]
                r.set_marks(api.payload["min_marks"], api.payload["max_marks"])
                r.is_active = False
                r.heat_list_published = previous_round.heat_list_published
                r.competition = previous_round.competition
                r.dances = previous_round.dances
                for dance in r.dances:
                    da = DanceActive()
                    da.round = r
                    da.dance = dance
                    r.dance_active.append(da)
                r.couples = previous_round.couples
                if api.payload["type"] == RoundType.final.name:
                    r.create_final()
                else:
                    r.create_heats(previous_round.number_of_heats(), floors=len(previous_round.floors()),
                                   different_heats=True)
                db.session.delete(previous_round)
                db.session.commit()
            return {
                "competition": r.competition.json(),
                "round": r.json(),
            }
        abort(404, "Unknown competition_id")


@api.route("/<int:round_id>/progress/couples")
@api.param("round_id", "Round id")
class RoundAPIProgressCouples(Resource):

    @api.doc("get_progress_couples")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get the couples that are participating in this round"""
        r = Round.query.get(round_id)
        if r is not None:
            return [c.json() for c in r.couples]
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/progress/couples/possible")
@api.param("round_id", "Round id")
class RoundAPIProgressCouplesPossible(Resource):

    @api.doc("get_progress_couples_possible")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get a list of couples that can be added to this round"""
        r = Round.query.get(round_id)
        if r is not None:
            return [c.json() for c in r.couples_that_can_be_added()]
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/progress/split")
@api.param("round_id", "Round id")
class RoundAPIProgressCouplesSplit(Resource):

    @api.doc("get_progress_split")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get the possible split options for a qualification round"""
        r = Round.query.get(round_id)
        if r is not None:
            return {
                "splits": r.split_options__html(),
                "competitions": [c.dancing_class.name for c in r.competition.sorted_qualifications()],
            }
        abort(404, "Unknown round_id")

    @api.doc("post_progress_split")
    @api.param("split", "Split option")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, round_id):
        """Split the qualification round"""
        r = Round.query.get(round_id)
        if r is not None:
            r.split_qualification(api.payload["split"])
            return {
                "competitions": [c.json() for c in r.competition.event.competitions_by_date()],
                "round": r.json()
            }
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/progress/couple/<int:couple_id>")
@api.param("round_id", "Specify the id of the Round.")
@api.param("couple_id", "Specify the id of the Couple.")
@api.response(200, "OK")
@api.response(404, "Round not found")
class RoundAPIProgressCoupleSpecific(Resource):

    @api.doc("patch_round_couple")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id, couple_id):
        """Add a couple to a round"""
        r = Round.query.get(round_id)
        if r is not None:
            c = Couple.query.get(couple_id)
            if c is not None:
                r.add_couple(c)
                return r.progress_data()
        abort(404, "Unknown round_id")

    @api.doc("delete_round_couple")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, round_id, couple_id):
        """Remove a couple from a round"""
        r = Round.query.get(round_id)
        if r is not None:
            c = Couple.query.get(couple_id)
            if c is not None:
                r.remove_couple(c)
                return r.progress_data()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/reports")
@api.param("round_id", "Round id")
class RoundAPIReports(Resource):

    @api.doc("get_reports")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get reports data"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.reports_data()
        abort(404, "Unknown round_id")

    @api.doc("patch_reports")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id):
        """Publishes or hides the heat list"""
        r = Round.query.get(round_id)
        if r is not None:
            r.heat_list_published = not r.heat_list_published
            db.session.commit()
            return OK
        abort(404, "Unknown round_id")

    @api.doc("post_reports")
    @api.param("prints", "List of reports to print")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, round_id):
        """Returns data to print reports"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.printing_data(api.payload["prints"])
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/floor_management")
@api.param("round_id", "Round id")
class RoundAPIFloorManagement(Resource):

    @api.doc("get_floor_management")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get floor management data for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            return {
                "round": r.json(),
                "data": r.floor_management_data(r.first_dance().dance_id),
            }
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/floor_management/dance/<int:dance_id>")
@api.param("dance_id", "Dance id")
@api.param("round_id", "Round id")
class RoundAPIFloorManagementDance(Resource):

    @api.doc("get_floor_management_dance")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_FLOOR_MANAGER])
    def get(self, round_id, dance_id):
        """Get floor management data for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.has_dance(dance_id):
                return r.floor_management_data(dance_id)
            abort(404, "Round does not have dance with given dance_id")
        abort(404, "Unknown round_id")

    @api.doc("patch_floor_management_dance")
    @api.param("couple_present_ids", "List of ids to mark present")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id, dance_id):
        """Marks list of couples as present for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.has_dance(dance_id):
                heats = [h.heat_id for h in r.heats if h.dance_id == dance_id]
                CouplePresent.query.filter(CouplePresent.heat_id.in_(heats))\
                    .update({CouplePresent.present: False}, synchronize_session='fetch')
                CouplePresent.query.filter(CouplePresent.couple_present_id.in_(api.payload["couple_present_ids"])) \
                    .update({CouplePresent.present: True}, synchronize_session='fetch')
                db.session.commit()
                return r.floor_management_data(dance_id)
            abort(404, "Round does not have dance with given dance_id")
        abort(404, "Unknown round_id")

    @api.doc("delete_floor_management_dance")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, round_id, dance_id):
        """Clear list of present couples for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.has_dance(dance_id):
                heats = [h.heat_id for h in r.heats if h.dance_id == dance_id]
                CouplePresent.query.filter(CouplePresent.heat_id.in_(heats))\
                    .update({CouplePresent.present: False}, synchronize_session='fetch')
                db.session.commit()
                return r.floor_management_data(dance_id)
            abort(404, "Round does not have dance with given dance_id")
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/floor_management/dance/<int:dance_id>/move")
@api.param("dance_id", "Dance id")
@api.param("round_id", "Round id")
class RoundAPIFloorManagementDanceMove(Resource):

    @api.doc("get_floor_management_dance_move")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id, dance_id):
        """Get floor management data for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.move_couple_data(dance_id)
        abort(404, "Unknown round_id")

    @api.doc("patch_floor_management_dance_move")
    @api.param("couple_id", "Id of the couple that is to be moved.")
    @api.param("from_id", "Id of the heat that the couple will be moved from.")
    @api.param("to_id", "Id of the heat that the couple will be moved to.")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id, dance_id):
        """Moves a couple between heats"""
        r = Round.query.get(round_id)
        if r is not None:
            from_heat = Heat.query.filter(Heat.heat_id == api.payload["from_id"]).first()
            to_heat = Heat.query.filter(Heat.heat_id == api.payload["to_id"]).first()
            if from_heat.round == to_heat.round and from_heat.dance == to_heat.dance:
                couple = Couple.query.filter(Couple.couple_id == api.payload["couple_id"]).first()
                marks = Mark.query.filter(Mark.couple == couple, Mark.heat == from_heat).all()
                for mark in marks:
                    mark.heat = to_heat
                present = CouplePresent.query.filter(CouplePresent.couple == couple,
                                                     CouplePresent.heat == from_heat).first()
                present.heat = to_heat
                from_heat.couples.remove(couple)
                to_heat.couples.append(couple)
                db.session.commit()
                return r.floor_management_data(dance_id)
            abort(400, "Heats to not belong to the same round")
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/adjudication")
@api.param("round_id", "Round id")
class RoundAPIAdjudication(Resource):

    @api.doc("get_adjudication")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id):
        """Get adjudication data for the first dance of the round"""
        r = Round.query.get(round_id)
        if r is not None:
            data = {
                "round": r.json(),
            }
            if r.is_general_look():
                data.update({
                    "data": {
                        "mapping": {},
                        "couples": [],
                    }
                })
            else:
                data.update({
                    "data": r.adjudication_data(r.first_dance().dance_id),
                })
            return data
        abort(404, "Unknown round_id")

    @api.doc("patch_adjudication")
    @api.param("min_marks", "Min target marks.")
    @api.param("max_marks", "Max target marks.")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id):
        """Update the target marks for the round"""
        r = Round.query.get(round_id)
        if r is not None:
            r.set_marks(api.payload["min_marks"], api.payload["max_marks"])
            db.session.commit()
            return r.json()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/adjudication/dance/<int:dance_id>/adjudicators")
@api.param("dance_id", "Dance id")
@api.param("round_id", "Round id")
class RoundAPIAdjudicationAdjudicators(Resource):

    @api.doc("get_adjudication_adjudicators")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id, dance_id):
        """Get adjudication data for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            return [a.adjudication_json(dancing_round=r, dance_id=dance_id) for a in r.sorted_adjudicators()]
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/adjudication/dance/<int:dance_id>")
@api.param("dance_id", "Dance id")
@api.param("round_id", "Round id")
class RoundAPIAdjudicationDance(Resource):

    @api.doc("get_adjudication_dance")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, round_id, dance_id):
        """Get adjudication data for a specific dance"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.has_dance(dance_id):
                return r.adjudication_data(dance_id, dancing_round=True)
            abort(404, "Round does not have dance with given dance_id")
        abort(404, "Unknown round_id")

    @api.doc("patch_adjudication_dance")
    @api.param("mark_ids", "List of ids to give a mark to")
    @api.param("placings", "List of dicts containing the final_placing_id and placement")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id, dance_id):
        """Gives a mark to a list of couples for a specific dance or placing for couples in the final"""
        r = Round.query.get(round_id)
        if r is not None:
            if r.has_dance(dance_id):
                if r.is_final():
                    r.save_placings(placings=api.payload["placings"], dance_id=dance_id)
                else:
                    heats = [h.heat_id for h in r.heats if h.dance_id == dance_id]
                    Mark.query.filter(Mark.heat_id.in_(heats)).update({Mark.mark: False}, synchronize_session='fetch')
                    Mark.query.filter(Mark.mark_id.in_(api.payload["mark_ids"]))\
                        .update({Mark.mark: True}, synchronize_session='fetch')
                    db.session.commit()
                return r.adjudication_data(dance_id, dancing_round=True)
            abort(404, "Round does not have dance with given dance_id")
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/adjudication/toggle")
@api.param("round_id", "Round id")
class RoundAPIAdjudicationToggleRound(Resource):

    @api.doc("patch_adjudication_toggle")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id):
        """Enable/Disable all dances for a round"""
        r = Round.query.get(round_id)
        if r is not None:
            r.toggle_active_dances()
            return r.json()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/adjudication/dance/<int:dance_id>/toggle")
@api.param("dance_id", "Dance id")
@api.param("round_id", "Round id")
class RoundAPIAdjudicationToggleDance(Resource):

    @api.doc("patch_adjudication_dance_toggle")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, round_id, dance_id):
        """Enable/Disable a dance of a round"""
        r = Round.query.get(round_id)
        if r is not None:
            r.toggle_active_dance(dance_id)
            return r.json()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/adjudication/evaluate")
@api.param("round_id", "Round id")
class RoundAPIAdjudicationEvaluateRound(Resource):

    @api.doc("round_adjudication_evaluate")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self, round_id):
        """Evaluate the result of a round"""
        r = Round.query.get(round_id)
        if r is not None:
            r.is_active = False;
            db.session.commit()
            if r.can_evaluate():
                r.evaluate()
                return OK
            abort(400, "Cannot evaluate round")
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/presenter")
@api.param("round_id", "Round id")
class RoundAPIPresenter(Resource):

    @api.doc("round_presenter")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER])
    def get(self, round_id):
        """Round for presenter"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.presenter_json()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/presenter/adjudicators")
@api.param("round_id", "Round id")
class RoundAPIPresenterAdjudicators(Resource):

    @api.doc("round_presenter_adjudicators")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER])
    def get(self, round_id):
        """Adjudicator data for presenter"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.presenter_adjudicators()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/presenter/starting_list")
@api.param("round_id", "Round id")
class RoundAPIPresenterStartingList(Resource):

    @api.doc("round_presenter_starting_list")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER])
    def get(self, round_id):
        """Starting list data for presenter"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.starting_list()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/presenter/couples_present")
@api.param("round_id", "Round id")
class RoundAPIPresenterCouplesPresent(Resource):

    @api.doc("round_presenter_couples_present")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER])
    def get(self, round_id):
        """Floor manager data for presenter"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.couples_present()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/presenter/no_re_dance_couples")
@api.param("round_id", "Round id")
class RoundAPIPresenterNoReDanceCouples(Resource):

    @api.doc("round_presenter_no_re_dance_couples")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER])
    def get(self, round_id):
        """No re-dance couples data for presenter"""
        r = Round.query.get(round_id)
        if r is not None:
            return r.no_re_dance_couples()
        abort(404, "Unknown round_id")


@api.route("/<int:round_id>/presenter/results")
@api.param("round_id", "Round id")
class RoundAPIPresenterResults(Resource):

    @api.doc("round_presenter_results")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER, AL_PRESENTER])
    def get(self, round_id):
        """Result data for presenter"""
        r = Round.query.get(round_id)
        if r is not None:
            return {
                "round": r.json(),
                "data": r.presenter_final_results(),
                "results": r.results(),
            }
        abort(404, "Unknown round_id")
