from flask_restplus import Namespace, Resource, abort
from backend.models.couple import Couple
from backend.models import db
from backend.models.dancer import Dancer
from backend.models.discipline import Discipline
from backend.models.dancing_class import DancingClass
from backend.models.competition import Competition
from backend.models.event import Event
from backend.constants import LEAD, FOLLOW, AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level


api = Namespace("couples", description="Couples")


def couples():
    return [c.json() for c in Couple.query.order_by(Couple.number).all()]


@api.route("/")
class CoupleListAPI(Resource):

    @api.doc("couples")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """All couples"""
        return couples()

    @api.doc("post_couple")
    @api.param("lead", "Lead_id")
    @api.param("follow", "Follow_id")
    @api.param("competitions", "List of competitions_ids")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new couple"""
        couple = Couple()
        couple.lead = Dancer.query.filter(Dancer.dancer_id == api.payload["lead"]).first()
        couple.follow = Dancer.query.filter(Dancer.dancer_id == api.payload["follow"]).first()
        couple.number = couple.lead.number
        comps = Competition.query.filter(Competition.competition_id.in_(api.payload["competitions"])).all()
        couple.set_competitions(comps)
        db.session.commit()
        event = Event.query.filter(Event.is_active.is_(True)).first()
        competitions = [c.json() for c in event.competitions_by_date()] if event is not None else []
        return {
            "couples": couples(),
            "competitions": competitions,
        }


@api.route("/<int:couple_id>")
class CoupleAPISpecific(Resource):

    @api.doc("get_couple")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self, couple_id):
        """Specific couple"""
        couple = Couple.query.get(couple_id)
        if couple is not None:
            return couple.couple_json()
        abort(404, "Unknown couple_id")

    @api.doc("patch_couple")
    @api.param("lead", "Lead_id")
    @api.param("follow", "Follow_id")
    @api.param("competitions", "List of competitions_ids")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, couple_id):
        """Update existing couple"""
        couple = Couple.query.get(couple_id)
        if couple is not None:
            couple.lead = Dancer.query.filter(Dancer.dancer_id == api.payload["lead"]).first()
            couple.follow = Dancer.query.filter(Dancer.dancer_id == api.payload["follow"]).first()
            couple.number = couple.lead.number
            comps = Competition.query.filter(Competition.competition_id.in_(api.payload["competitions"])).all()
            couple.set_competitions(comps)
            db.session.commit()
            event = Event.query.filter(Event.is_active.is_(True)).first()
            competitions = [c.json() for c in event.competitions_by_date()] if event is not None else []
            return {
                "couple": couple.json(),
                "competitions": competitions,
            }
        abort(404, "Unknown dancer_id")

    @api.doc("delete_couple")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, couple_id):
        """Delete dancer"""
        couple = Couple.query.get(couple_id)
        if couple is not None:
            if couple.deletable():
                db.session.delete(couple)
                db.session.commit()
                return couple_id
            abort(400, "Couple cannot be deleted.")
        abort(404, "Unknown couple_id")


@api.route("/csv")
class CoupleCSV(Resource):

    @api.doc("post_dancers")
    @api.param("csv", "List of csv strings")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new couples from list of csv strings"""
        import_list = api.payload["csv"].split("\n")
        counter = 0
        for import_string in import_list:
            data = import_string.split(',')
            data = [d.strip() for d in data]
            if len(data) >= 2:
                lead_number = data[0]
                follow_number = data[1]
                check_lead = Dancer.query.filter(Dancer.number == lead_number, Dancer.role == LEAD).first()
                check_follow = Dancer.query.filter(Dancer.number == follow_number, Dancer.role == FOLLOW).first()
                if check_lead is not None and check_follow is not None:
                    couple = Couple.query.filter(Couple.lead == check_lead, Couple.follow == check_follow).first()
                    if couple is None:
                        couple = Couple()
                        couple.lead = check_lead
                        couple.follow = check_follow
                        couple.number = check_lead.number
                    counter += 1
                    if len(data) == 4:
                        discipline = data[2].strip()
                        dancing_class = data[3].strip()
                        check_competition = Competition.query.join(Discipline, DancingClass) \
                            .filter(Discipline.name == discipline, DancingClass.name == dancing_class).first()
                        if check_competition is not None:
                            couple.competitions.append(check_competition)
                    db.session.add(couple)
        db.session.commit()
        return {
            "couples": couples(),
            "added": counter,
        }
