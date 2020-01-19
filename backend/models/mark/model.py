from backend.models.base import db, TrackModifications, TABLE_MARK


class Mark(db.Model, TrackModifications):
    __tablename__ = TABLE_MARK
    mark_id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Integer, default=0)
    adjudicator_id = db.Column(db.Integer, db.ForeignKey("adjudicator.adjudicator_id",
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    adjudicator = db.relationship("Adjudicator")
    couple_id = db.Column(db.Integer, db.ForeignKey("couple.couple_id", onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    heat_id = db.Column(db.Integer, db.ForeignKey("heat.heat_id", onupdate="CASCADE", ondelete="CASCADE"))
    heat = db.relationship("Heat", back_populates="marks")

    def __repr__(self):
        return "{round} - {dance} - {adj} - {couple}"\
            .format(couple=self.couple, adj=self.adjudicator.name, dance=self.heat.dance, round=self.heat.round)

    def json(self):
        data = {
            "mark_id": self.mark_id,
            "mark": self.mark,
            "notes": self.notes,
            "number": self.couple.number,
            "follow_number": self.couple.follow.number,
        }
        return data
