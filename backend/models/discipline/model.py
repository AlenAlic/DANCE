from backend.models.base import db, TrackModifications, TABLE_DISCIPLINE


class Discipline(db.Model, TrackModifications):
    __tablename__ = TABLE_DISCIPLINE
    discipline_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    tag = db.Column(db.String(12), unique=True, nullable=False)
    competitions = db.relationship("Competition", back_populates="discipline")
    dances = db.relationship("Dance", back_populates="discipline")

    def __repr__(self):
        return f"{self.name}"

    def json(self):
        data = {
            "discipline_id": self.discipline_id,
            "name": self.name,
            "tag": self.tag,
            "has_competitions": self.has_competitions(),
            "has_dances": self.has_dances(),
            "deletable": self.deletable(),
            "dances": [{"dance_id": d.dance_id, "name": d.name} for d in self.dances]
        }
        return data

    def has_competitions(self):
        return len(self.competitions) > 0

    def has_dances(self):
        return len(self.dances) > 0

    def deletable(self):
        return not self.has_competitions()
