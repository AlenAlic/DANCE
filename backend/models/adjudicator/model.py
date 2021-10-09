from backend.models.base import db, TrackModifications, TABLE_ADJUDICATOR
from backend.models.competition import competition_adjudicator_table
from backend.models.round import Round
from backend.models.dance import Dance
from backend.util import datetime_browser


class Adjudicator(db.Model, TrackModifications):
    __tablename__ = TABLE_ADJUDICATOR
    adjudicator_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    tag = db.Column(db.String(6), unique=True)
    dance = db.Column(db.Integer, nullable=False, default=0)
    round = db.Column(db.Integer, nullable=False, default=0)
    competitions = db.relationship("Competition", secondary=competition_adjudicator_table,
                                   back_populates="adjudicators")
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", backref=db.backref("adjudicator", uselist=False), single_parent=True,
                           cascade="all, delete-orphan")
    assignments = db.relationship("AdjudicatorCompetitionAssignment", back_populates="adjudicator")

    def __repr__(self):
        return f"{self.name}"

    def json(self):
        data = {
            "adjudicator_id": self.adjudicator_id,
            "name": self.name,
            "tag": self.tag,
            "dance": self.current_dance(),
            "round": self.current_round(),
            "competitions": [{
                "competition_id": c.competition_id,
                "name": c.name()
            } for c in self.sorted_competitions()],
            "has_competitions": self.has_competitions(),
            "grouped_competitions": self.grouped_competitions(),
            "deletable": self.deletable(),
        }
        return data

    def has_competitions(self):
        return len(self.competitions) > 0

    def sorted_competitions(self):
        return list(sorted([c for c in self.competitions], key=lambda x: x.when))

    def grouped_competitions(self):
        dates = list(sorted(set([c.when.date() for c in self.competitions])))
        return [{
            "date": datetime_browser(d),
            "competitions": [
                {
                    "competition_id": c.competition_id,
                    "name": c.name(),
                    "last_round": {
                        "round_id": c.last_round().round_id,
                        "name": c.last_round().type.value,
                        "is_active": c.last_round().is_active,
                        "first_dance": c.last_round().first_active_dance().json()
                        if c.last_round().first_active_dance() else None
                    } if c.last_round() else None,
                } for c in self.competitions if c.when.date() == d]
        } for d in dates]

    def current_round(self):
        if self.round != 0:
            return f"{Round.query.filter(Round.round_id == self.round).first()}"
        return None

    def current_dance(self):
        if self.dance != 0:
            return f"{Dance.query.filter(Dance.dance_id == self.dance).first()}"
        return None

    def deletable(self):
        return len(self.competitions) == 0

    def active_round(self):
        if self.round != 0:
            return f"{Round.query.filter(Round.round_id == self.round).first()}"
        return None

    def active_dance(self):
        if self.dance != 0:
            return f"{Dance.query.filter(Dance.dance_id == self.dance).first()}"
        return None

    def is_present(self, r, dance_id=0):
        if dance_id > 0:
            return r.round_id == self.round and dance_id == self.dance
        return r.round_id == self.round
