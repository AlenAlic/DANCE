from backend.models.base import db, TrackModifications, TABLE_ADJUDICATOR_COMPETITION_ASSIGNMENT
from .enums import AdjudicatorAssignmentEnum


class AdjudicatorCompetitionAssignment(db.Model, TrackModifications):
    __tablename__ = TABLE_ADJUDICATOR_COMPETITION_ASSIGNMENT
    adjudicator_competition_assignment_id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.String(48), nullable=True, default=None)
    assignment = db.Column(db.Enum(AdjudicatorAssignmentEnum), default=AdjudicatorAssignmentEnum.both)
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.competition_id",
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    competition = db.relationship("Competition", back_populates="adjudicator_assignments")
    adjudicator_id = db.Column(db.Integer, db.ForeignKey("adjudicator.adjudicator_id",
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    adjudicator = db.relationship("Adjudicator", back_populates="assignments")

    def __repr__(self):
        return f"{self.adjudicator.name} - {self.competition} - {self.floor} - {self.assignment.name}"

    def json(self):
        data = {
            "adjudicator_competition_assignment_id": self.adjudicator_competition_assignment_id,
            "floor": self.floor,
            "assignment": self.assignment.name,
            "adjudicator_id": self.adjudicator.adjudicator_id,
            "name": self.adjudicator.name,
            "tag": self.adjudicator.tag,
        }
        return data

    def adjudication_json(self, dancing_round, dance_id):
        return {
            "adjudicator_id": self.adjudicator.adjudicator_id,
            "name": self.adjudicator.name,
            "is_present": self.adjudicator.is_present(dancing_round, dance_id),
            "floor": self.floor,
            "assignment": self.assignment.name,
        }
