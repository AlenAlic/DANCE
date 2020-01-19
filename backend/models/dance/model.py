from backend.models.base import db, TrackModifications, TABLE_DANCE


class Dance(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCE
    dance_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    tag = db.Column(db.String(6), unique=True)
    order = db.Column(db.Integer, nullable=False, default=0)
    discipline_id = db.Column(db.Integer, db.ForeignKey("discipline.discipline_id",
                                                        onupdate="CASCADE", ondelete="CASCADE"))
    discipline = db.relationship("Discipline", back_populates="dances")

    def __repr__(self):
        return f"{self.name}"

    def json(self):
        data = {
            "dance_id": self.dance_id,
            "name": self.name,
            "tag": self.tag,
            "order": self.order,
            "deletable": self.deletable(),
        }
        if self.has_discipline():
            data.update({
                "discipline": self.discipline.json()
            })
        return data

    def has_discipline(self):
        return self.discipline is not None

    def deletable(self):
        if not self.has_discipline():
            return True
        return self.discipline.deletable()
