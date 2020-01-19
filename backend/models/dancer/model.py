from backend.models.base import db, TrackModifications, TABLE_DANCER
from backend.models.competition import competition_lead_table, competition_follow_table
from backend.constants import LEAD


class Dancer(db.Model, TrackModifications):
    __tablename__ = TABLE_DANCER
    __table_args__ = (db.UniqueConstraint("number", "role", name="_number_role_uc"),)
    dancer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    number = db.Column(db.Integer)
    role = db.Column(db.String(128))
    team = db.Column(db.String(128))
    couples_lead = db.relationship("Couple", foreign_keys="Couple.lead_id", back_populates="lead")
    couples_follow = db.relationship("Couple", foreign_keys="Couple.follow_id", back_populates="follow")
    competitions_lead = db.relationship("Competition", secondary=competition_lead_table, back_populates="leads")
    competitions_follow = db.relationship("Competition", secondary=competition_follow_table, back_populates="follows")

    def __repr__(self):
        return f"{self.number}: {self.name}"
    
    def competition_name(self):
        return self.__repr__()

    def json(self):
        data = {
            "dancer_id": self.dancer_id,
            "number": self.number,
            "name": self.name,
            "competition_name": self.competition_name(),
            "role": self.role,
            "team": self.team,
        }
        return data

    def dancer_json(self):
        data = self.json()
        data.update({
            "competitions": [{
                "competition_id": c.competition_id,
                "name": c.name(),
            } for c in self.competitions()],
            "deletable": self.deletable(),
            "partners": [{
                "dancer_id": p["dancer"].dancer_id,
                "name": p["dancer"].name,
                "number": p["dancer"].number,
                "competitions": [c.name() for c in p["competitions"]]
            } for p in self.partners_list()],
        })
        return data

    def partners_list(self):
        if self.role == LEAD:
            return [{"dancer": c.follow, "competitions": c.participating_competitions()} for c in self.couples_lead]
        else:
            return [{"dancer": c.lead, "competitions": c.participating_competitions()} for c in self.couples_follow]

    def couples(self):
        if self.role == LEAD:
            return self.couples_lead
        else:
            return self.couples_follow

    def competitions(self):
        if self.role == LEAD:
            return self.competitions_lead
        else:
            return self.competitions_follow

    def deletable(self):
        return len(self.competitions_lead) + len(self.competitions_follow) + \
               len(self.couples_lead) + len(self.couples_follow) == 0

    def set_competitions(self, comps):
        if self.role == LEAD:
            self.competitions_lead = [c for c in self.competitions_lead if c.has_rounds()] + comps
        else:
            self.competitions_follow = [c for c in self.competitions_follow if c.has_rounds()] + comps
