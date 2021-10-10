from backend.models.base import db, TrackModifications, TABLE_COUPLE
from backend.models.competition.links import competition_couple_table
from backend.models.round.links import round_couple_table
from backend.models.heat.links import heat_couple_table
from backend.constants import TEST


class Couple(db.Model, TrackModifications):
    __tablename__ = TABLE_COUPLE
    __table_args__ = (db.UniqueConstraint("lead_id", "follow_id", name="_lead_follow_uc"),)
    couple_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    lead_id = db.Column(db.Integer, db.ForeignKey("dancer.dancer_id", onupdate="CASCADE", ondelete="CASCADE"))
    lead = db.relationship("Dancer", back_populates="couples_lead", foreign_keys="Couple.lead_id")
    follow_id = db.Column(db.Integer, db.ForeignKey("dancer.dancer_id", onupdate="CASCADE", ondelete="CASCADE"))
    follow = db.relationship("Dancer",  back_populates="couples_follow", foreign_keys="Couple.follow_id")
    competitions = db.relationship("Competition", secondary=competition_couple_table, back_populates="couples")
    rounds = db.relationship("Round", secondary=round_couple_table, back_populates="couples")
    heats = db.relationship("Heat", secondary=heat_couple_table)

    def __repr__(self):
        return "{number}: {lead} / {follow}".format(number=self.number, lead=self.lead.name, follow=self.follow.name)

    def name(self):
        return self.__repr__()

    def json(self):
        data = {
            "couple_id": self.couple_id,
            "name": self.name(),
            "number": self.number,
            "team": self.team(),
            "lead": {
                "dancer_id": self.lead.dancer_id,
                "number": self.lead.number,
                "team": self.lead.team,
                "name": self.lead.name,
            },
            "follow": {
                "dancer_id": self.follow.dancer_id,
                "number": self.follow.number,
                "team": self.follow.team,
                "name": self.follow.name,
            },
        }
        return data

    def couple_json(self):
        data = self.json()
        data.update({
            "deletable": self.deletable(),
            "competitions": [{
                "competition_id": c.competition_id,
                "name": c.name()
            } for c in self.participating_competitions()],
        })
        return data

    def presenter_json(self):
        data = {
            "couple_id": self.couple_id,
            "name": self.names(),
            "number": self.number,
            "team": self.team(),
        }
        return data

    def starting_list_json(self):
        data = {
            "couple_id": self.couple_id,
            "number": self.number,
            "name": self.names(),
            "team": self.team(),
            "lead": {
                "name": self.lead.name,
                "team": self.lead.team
            },
            "follow": {
                "name": self.follow.name,
                "team": self.follow.team
            },
        }
        return data

    def team(self):
        if self.lead.team == self.follow.team:
            return self.lead.team
        else:
            return f"{self.lead.team} / {self.follow.team}"

    def participating_competitions(self):
        if len(self.competitions) > 0:
            return [c for c in self.competitions if c.dancing_class.name != TEST]
        else:
            return list(set([r.competition for r in self.rounds + [h.round for h in self.heats]]))

    def deletable(self):
        return len(self.rounds) == 0 and len(self.heats) == 0

    def names(self):
        return f"{self.lead.name} / {self.follow.name}"

    def set_competitions(self, comps):
        self.competitions = [c for c in self.competitions if c.has_rounds()] + comps
