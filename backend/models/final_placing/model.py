from backend.models.base import db, TrackModifications, TABLE_FINAL_PLACING


class FinalPlacing(db.Model, TrackModifications):
    __tablename__ = TABLE_FINAL_PLACING
    final_placing_id = db.Column(db.Integer, primary_key=True)
    final_placing = db.Column(db.Integer, default=0)
    adjudicator_id = db.Column(db.Integer, db.ForeignKey("adjudicator.adjudicator_id",
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    adjudicator = db.relationship("Adjudicator")
    couple_id = db.Column(db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    round_id = db.Column(db.Integer, db.ForeignKey("round.round_id", onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="final_placings")
    dance_id = db.Column(db.Integer, db.ForeignKey("dance.dance_id", onupdate="CASCADE", ondelete="CASCADE"))
    dance = db.relationship("Dance")

    def __repr__(self):
        return "{round} - {dance} - {adj} - {couple}"\
            .format(couple=self.couple, adj=self.adjudicator.name, dance=self.dance, round=self.round)

    def json(self):
        data = {
            "final_placing_id": self.final_placing_id,
            "final_placing": self.final_placing,
            "number": self.couple.number,
            "follow_number": self.couple.follow.number,
        }
        return data
