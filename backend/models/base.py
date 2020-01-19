from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime


db = SQLAlchemy()
login = LoginManager()


class TrackModifications(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


TABLE_USER = "user"
TABLE_EVENT = "event"
TABLE_EVENT_RESULT = "event_result"
TABLE_COMPETITION = "competition"
TABLE_DANCING_CLASS = "dancing_class"
TABLE_DISCIPLINE = "discipline"
TABLE_DANCE = "dance"
TABLE_ADJUDICATOR = "adjudicator"
TABLE_ADJUDICATOR_COMPETITION_ASSIGNMENT = "adjudicator_competition_assignment"
TABLE_DANCER = "dancer"
TABLE_COUPLE = "couple"
TABLE_ROUND = "round"
TABLE_DANCE_ACTIVE = "dance_active"
TABLE_HEAT = "heat"
TABLE_MARK = "mark"
TABLE_FINAL_PLACING = "final_placing"
TABLE_COUPLE_PRESENT = "couple_present"
TABLE_ROUND_RESULT = "round_result"

TABLE_COMPETITION_LEAD = "competition_lead"
TABLE_COMPETITION_FOLLOW = "competition_follow"
TABLE_COMPETITION_COUPLE = "competition_couple"
TABLE_COMPETITION_ADJUDICATOR = "competition_adjudicator"
TABLE_ROUND_DANCE = "round_dance"
TABLE_ROUND_COUPLE = "round_couple"
TABLE_HEAT_COUPLE = "heat_couple"


ADJUDICATOR_SYSTEM_TABLES = [
    TABLE_COMPETITION,
    TABLE_DANCING_CLASS,
    TABLE_DISCIPLINE,
    TABLE_DANCE,
    TABLE_ADJUDICATOR,
    TABLE_DANCER,
    TABLE_COUPLE,
    TABLE_ROUND,
    TABLE_DANCE_ACTIVE,
    TABLE_HEAT,
    TABLE_MARK,
    TABLE_FINAL_PLACING,
    TABLE_COUPLE_PRESENT,
    TABLE_ROUND_RESULT,
    TABLE_COMPETITION_LEAD,
    TABLE_COMPETITION_FOLLOW,
    TABLE_COMPETITION_COUPLE,
    TABLE_COMPETITION_ADJUDICATOR,
    TABLE_ROUND_DANCE,
    TABLE_ROUND_COUPLE,
    TABLE_HEAT_COUPLE,
]
