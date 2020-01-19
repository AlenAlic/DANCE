from backend.models.base import db, TrackModifications, TABLE_COUPLE_PRESENT
from backend.models.heat import Heat


class CouplePresent(db.Model, TrackModifications):
    __tablename__ = TABLE_COUPLE_PRESENT
    couple_present_id = db.Column(db.Integer, primary_key=True)
    present = db.Column(db.Boolean, default=False)
    couple_id = db.Column(db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    heat_id = db.Column(db.Integer, db.ForeignKey("heat.heat_id", onupdate="CASCADE", ondelete="CASCADE"))
    heat = db.relationship("Heat", back_populates="couples_present")

    def __repr__(self):
        return f"{self.heat.round} - {self.heat.dance} - {self.couple}"

    def json(self):
        data = {
            "couple_present_id": self.couple_present_id,
            "number": self.couple_number(),
            "name": self.couple_name(),
            "present": self.present,
            "heat": self.heat.number,
            "floor": self.heat.floor
        }
        return data

    def couple_number(self):
        if self.heat.round.competition.is_change_per_dance():
            return f"{self.couple.lead.number} / {self.couple.follow.number}"
        return self.couple.number

    def couple_name(self):
        return f"{self.couple.lead.name} / {self.couple.follow.name}"

    def mark_in_next_heat(self, present):
        r = self.heat.round
        c = r.competition
        if not c.is_change_per_dance() and self.heat.dance != r.last_dance():
            num = int(r.number_of_heats() / r.number_of_floors())
            if self.heat.number == num:
                cp = CouplePresent.query.join(Heat)\
                    .filter(Heat.dance == r.next_dance(self.heat.dance), Heat.number == 1,
                            CouplePresent.couple == self.couple).first()
                if cp is not None:
                    cp.present = present
