from backend.models.base import db, TrackModifications, TABLE_EVENT_RESULT


class EventResult(db.Model, TrackModifications):
    __tablename__ = TABLE_EVENT_RESULT
    event_result_id = db.Column(db.Integer, primary_key=True)
    competition = db.Column(db.String(128))
    date = db.Column(db.DateTime)
    result = db.Column(db.JSON, nullable=True, default=None)
    event_id = db.Column(db.Integer, db.ForeignKey("event.event_id", onupdate="CASCADE", ondelete="CASCADE"))
    event = db.relationship("Event", back_populates="results", single_parent=True)

    def __repr__(self):
        return f"{self.competition}"

    def json(self, results=False):
        data = {
            "event_result_id": self.event_result_id,
            "competition": self.competition,
            "event": self.event.name,
        }
        if results:
            data.update({
                "result": self.result
            })
        return data

    def save_results(self, comp):
        self.competition = comp.name()
        self.date = comp.when
        self.result = comp.results_string if comp.results_string else comp.results()
        comp.event.results.append(self)
