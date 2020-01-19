from backend.models.base import db, TrackModifications, TABLE_DANCING_CLASS


class DancingClass(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCING_CLASS
    dancing_class_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    tag = db.Column(db.String(12), unique=True, nullable=False)
    competitions = db.relationship("Competition", back_populates="dancing_class")

    def __repr__(self):
        return f"{self.name}"

    def json(self):
        data = {
            "dancing_class_id": self.dancing_class_id,
            "name": self.name,
            "tag": self.tag,
            "has_competitions": self.has_competitions(),
            "deletable": self.deletable()
        }
        return data

    def has_competitions(self):
        return len(self.competitions) > 0

    def deletable(self):
        return not self.has_competitions()
