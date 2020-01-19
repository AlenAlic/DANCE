from backend.models.base import db, TrackModifications, TABLE_ROUND_RESULT


class RoundResult(db.Model, TrackModifications):
    __tablename__ = TABLE_ROUND_RESULT
    round_result_id = db.Column(db.Integer, primary_key=True)
    couple_id = db.Column(db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    marks = db.Column(db.Integer, default=0)
    placing = db.Column(db.String(12))
    total = db.Column(db.Float, default=0.0)
    final_placing = db.Column(db.Float, default=0.0)
    follow = db.Column(db.Boolean, default=False)
    round_id = db.Column(db.Integer, db.ForeignKey("round.round_id", onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="round_results")

    def __repr__(self):
        return "{round} - {couple}".format(couple=self.couple, round=self.round)

    def json(self):
        data = {
            "round_result_id": self.round_result_id,
            "couple": self.couple.json(),
            "follow": self.follow,
        }
        if self.round.is_final():
            data.update({
                "total": self.total,
                "final_placing": self.final_placing,
            })
        else:
            data.update({
                "marks": self.marks,
                "placing": self.placing,
            })
        return data
