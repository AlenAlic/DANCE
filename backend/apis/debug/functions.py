from backend.test_data import ADJUDICATORS, COUPLES
from backend.constants import AL_ADJUDICATOR, LEAD, FOLLOW
from backend.models import db
from backend.models.user import User
from backend.models.adjudicator import Adjudicator
from backend.models.dancer import Dancer
from backend.models.couple import Couple


def create_adjudicators():
    for adj in ADJUDICATORS:
        adjudicator = Adjudicator()
        adjudicator.name = adj['name']
        adjudicator.tag = adj['tag']
        user = User()
        user.username = adjudicator.tag
        user.set_password(adjudicator.tag)
        user.is_active = True
        user.access = AL_ADJUDICATOR
        user.adjudicator = adjudicator
        db.session.add(user)
        db.session.commit()


def create_couples():
    for c in COUPLES:
        lead = Dancer()
        lead.name = c['lead']
        lead.role = LEAD
        lead.team = c['lead_team']
        lead.number = c['number']
        db.session.add(lead)
        follow = Dancer()
        follow.name = c['follow']
        follow.role = FOLLOW
        follow.team = c['follow_team']
        follow.number = c['number'] + len(COUPLES) + 200
        db.session.add(follow)
        couple = Couple()
        couple.number = lead.number
        couple.lead = lead
        couple.follow = follow
        db.session.add(couple)
        db.session.commit()
