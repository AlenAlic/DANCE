from backend.models.base import db, TrackModifications, TABLE_HEAT
from .links import heat_couple_table


class Heat(db.Model, TrackModifications):
    __tablename__ = TABLE_HEAT
    heat_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, default=1)
    round_id = db.Column(db.Integer, db.ForeignKey("round.round_id", onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="heats")
    dance_id = db.Column(db.Integer, db.ForeignKey("dance.dance_id"))
    dance = db.relationship("Dance")
    floor = db.Column(db.String(48), nullable=True, default=None)
    couples = db.relationship("Couple", secondary=heat_couple_table)
    marks = db.relationship("Mark", back_populates="heat", cascade="all, delete, delete-orphan")
    couples_present = db.relationship("CouplePresent", back_populates="heat", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "{round} - {dance} - Heat {number}".format(number=self.number, dance=self.dance, round=self.round)

    def json(self):
        data = {
            "heat_id": self.heat_id,
            "number": self.heat_number()
        }
        return data

    def heat_number(self):
        return self.number if self.floor is None else f"{self.number}.{self.floor}"

    def ordered_couples_present(self):
        return list(sorted(self.couples_present, key=lambda c: c.couple.number))

    def ordered_marks(self, adjudicator):
        return list(sorted([m for m in self.marks if m.adjudicator == adjudicator] if adjudicator else self.marks,
                           key=lambda c: c.couple.number))

    def ordered_dancers(self):
        dancers = [c.lead for c in self.couples] + [c.follow for c in self.couples]
        return list(sorted(dancers, key=lambda d: d.number))
