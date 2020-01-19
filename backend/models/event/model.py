from backend.models.base import db, TrackModifications, TABLE_EVENT
from backend.util import datetime_browser
from datetime import datetime


class Event(db.Model, TrackModifications):
    __tablename__ = TABLE_EVENT
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date().today())
    competitions = db.relationship("Competition", back_populates="event", cascade="all, delete, delete-orphan")
    results = db.relationship("EventResult", back_populates="event", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"{self.name}"

    def has_competitions(self):
        return len(self.competitions) > 0

    def unique_dates(self):
        return list(sorted(set([datetime_browser(c.when.date()) for c in self.competitions])))

    def competitions_by_date(self):
        return list(sorted([c for c in self.competitions], key=lambda x: x.when))

    def json(self):
        return {
            "event_id": self.event_id,
            "name": self.name,
            "date": self.date.isoformat(),
            "is_active": self.is_active,
            "has_competitions": self.has_competitions(),
            "unique_dates": self.unique_dates(),
        }

    def sorted_results(self):
        return list(sorted([r for r in self.results], key=lambda x: x.date))
