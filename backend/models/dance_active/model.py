from backend.models.base import db, TrackModifications, TABLE_DANCE_ACTIVE


class DanceActive(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCE_ACTIVE
    dance_active_id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False)
    round_id = db.Column(db.Integer, db.ForeignKey("round.round_id", onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="dance_active")
    dance_id = db.Column(db.Integer, db.ForeignKey("dance.dance_id", onupdate="CASCADE", ondelete="CASCADE"))
    dance = db.relationship("Dance")

    def __repr__(self):
        return "{round} - {dance}".format(round=self.round, dance=self.dance)

    def json(self):
        data = {
            "dance_id": self.dance.dance_id,
            "name": self.dance.name,
            "tag": self.dance.tag,
            "is_active": self.is_active,
        }
        return data
