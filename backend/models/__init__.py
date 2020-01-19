from .base import db, login
from .base import ADJUDICATOR_SYSTEM_TABLES
from .user import User
from .user.wrappers import requires_access_level, requires_adjudicator_access_level
from .event import Event
from .competition import Competition
from .competition.enums import CompetitionMode
from .dancing_class import DancingClass
from .discipline import Discipline
from .dance import Dance
from .adjudicator import Adjudicator
from .dancer import Dancer
from .couple import Couple
from .round import Round
from .round.enums import RoundType
from .dance_active import DanceActive
from .heat import Heat
from .mark import Mark
from .final_placing import FinalPlacing
from .couple_present import CouplePresent
from .round_result import RoundResult
from .adjudicator_competition_assignment import AdjudicatorCompetitionAssignment
from .event_result import EventResult


def init_app(app):
    db.init_app(app)
    login.init_app(app)


def active_event():
    return Event.query.filter(Event.is_active.is_(True)).first()
