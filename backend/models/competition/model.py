from backend.models.base import db, TrackModifications, TABLE_COMPETITION
from .links import competition_couple_table, competition_lead_table, competition_follow_table, \
    competition_adjudicator_table
from .enums import CompetitionMode
from backend.models.round import Round
from backend.models.couple.functions import generate_new_couples_from_dancers
from backend.models.round.model import RoundType
from backend.models.adjudicator_competition_assignment import AdjudicatorCompetitionAssignment
from backend.skating import CompetitionResult
import datetime
from backend.util import datetime_browser
import random
from backend.constants import LEAD, FOLLOW
from backend.models.adjudicator_competition_assignment.enums import AdjudicatorAssignmentEnum


class Competition(db.Model, TrackModifications):
    __tablename__ = TABLE_COMPETITION
    competition_id = db.Column(db.Integer, primary_key=True)
    dancing_class_id = db.Column(db.Integer, db.ForeignKey("dancing_class.dancing_class_id",
                                                           onupdate="CASCADE", ondelete="CASCADE"))
    dancing_class = db.relationship("DancingClass", back_populates="competitions")
    discipline_id = db.Column(db.Integer, db.ForeignKey("discipline.discipline_id",
                                                        onupdate="CASCADE", ondelete="CASCADE"))
    discipline = db.relationship("Discipline", back_populates="competitions")
    floors = db.Column(db.Integer, default=1)
    when = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    rounds = db.relationship("Round", back_populates="competition", cascade="all, delete, delete-orphan")
    mode = db.Column(db.Enum(CompetitionMode), default=CompetitionMode.single_partner)
    test = db.Column(db.Boolean, nullable=False, default=False)
    couples = db.relationship("Couple", secondary=competition_couple_table, back_populates="competitions")
    leads = db.relationship("Dancer", secondary=competition_lead_table, back_populates="competitions_lead")
    follows = db.relationship("Dancer", secondary=competition_follow_table, back_populates="competitions_follow")
    adjudicators = db.relationship("Adjudicator", secondary=competition_adjudicator_table)
    adjudicator_assignments = db.relationship("AdjudicatorCompetitionAssignment", back_populates="competition",
                                              cascade="all, delete, delete-orphan")
    event_id = db.Column(db.Integer, db.ForeignKey("event.event_id", onupdate="CASCADE", ondelete="CASCADE"))
    event = db.relationship("Event", back_populates="competitions", single_parent=True)
    qualification_id = db.Column(db.Integer, db.ForeignKey("competition.competition_id",
                                                           onupdate="CASCADE", ondelete="CASCADE"))
    qualifications = db.relationship("Competition", backref=db.backref("qualification", remote_side=[competition_id]))
    results_published = db.Column(db.Boolean, nullable=False, default=False)
    results_string = db.Column(db.JSON, nullable=True, default=None)

    def __repr__(self):
        return "{disc} {cls}".format(cls=self.dancing_class, disc=self.discipline)

    def name(self):
        return self.__repr__()

    def json(self):
        data = {
            "competition_id": self.competition_id,
            "name": self.name(),
            "discipline": self.discipline.json(),
            "dancing_class": self.dancing_class.json(),
            "floors": self.floors,
            "date": datetime_browser(self.when),
            "mode": self.mode.name,
            "qualification_id": self.qualification_id,
            "adjudicators": [{
                "adjudicator_competition_assignment_id": a.adjudicator_competition_assignment_id,
                "adjudicator_id": a.adjudicator.adjudicator_id,
                "name": a.adjudicator.name,
                "floor": a.floor,
                "assignment": a.assignment.name,
            } for a in self.sorted_adjudicators()],
            "couples": [{
                "couple_id": c.couple_id,
                "name": c.name(),
            } for c in self.sorted_couples()],
            "leads": [{
                "dancer_id": d.dancer_id,
                "name": d.competition_name(),
                "number": d.number,
            } for d in self.sorted_leads()],
            "follows": [{
                "dancer_id": d.dancer_id,
                "name": d.competition_name(),
                "number": d.number,
            } for d in self.sorted_follows()],
            "max_couples": self.max_couples(),
            "number_of_competitors": self.number_of_competitors(),
            "has_rounds": self.has_rounds(),
            "rounds": [r.json() for r in self.rounds],
            "last_round": self.last_round_json(),
            "can_create_first_round": self.can_create_first_round(),
            "updated": datetime_browser(self.updated_at),
            "has_adjudicators": self.has_adjudicators(),
            "adjudicators_assigned": self.adjudicators_assigned(),
            "is_quali": self.is_quali(),
            "show_starting_list": self.show_starting_list(),
        }
        return data

    def discipline_json(self):
        return {
            "discipline_id": self.discipline.discipline_id,
            "name": self.discipline.name,
        }

    def publish_json(self):
        data = {
            "competition_id": self.competition_id,
            "name": self.name(),
            "mode": self.mode.name,
            "results_published": self.results_published,
            "publishable": self.publishable()
        }
        return data

    def starting_lists_json(self):
        return {
            "competition_id": self.competition_id,
            "name": self.name(),
            "mode": self.mode.name,
            "starting_list_visible": self.starting_list_visible(),
            "has_rounds": self.has_rounds(),
        }

    def heat_lists_json(self):
        data = {
            "competition_id": self.competition_id,
            "name": self.name(),
            "mode": self.mode.name,
        }
        r = self.last_round_with_heat_list_published()
        data.update({
            "round": r.json() if r is not None else None
        })
        return data

    def update_adjudicator_assignments(self):
        assignments = [a.adjudicator for a in self.adjudicator_assignments]
        for a in self.adjudicators:
            if a not in assignments:
                assignment = AdjudicatorCompetitionAssignment()
                assignment.adjudicator = a
                assignment.competition = self
        for a in self.adjudicator_assignments:
            if a.adjudicator not in self.adjudicators:
                db.session.delete(a)

    def is_single_partner(self):
        return self.mode == CompetitionMode.single_partner

    def is_random_single_partner(self):
        return self.mode == CompetitionMode.random_single_partner

    def is_change_per_round(self):
        return self.mode == CompetitionMode.change_per_round

    def is_change_per_dance(self):
        return self.mode == CompetitionMode.change_per_dance

    def is_change_per(self):
        return self.is_change_per_round() or self.is_change_per_dance()

    def first_round(self):
        try:
            return Round.query.get(min([r.round_id for r in self.rounds]))
        except ValueError:
            return None

    def last_round(self):
        try:
            return Round.query.get(max([r.round_id for r in self.rounds]))
        except ValueError:
            return None

    def first_round_json(self):
        try:
            return self.first_round().json()
        except AttributeError:
            return None

    def last_round_json(self):
        try:
            return self.last_round().json()
        except AttributeError:
            return None

    def sorted_adjudicators(self):
        return sorted(self.adjudicator_assignments, key=lambda a: a.adjudicator.name)

    def sorted_qualifications(self):
        return sorted(self.qualifications, key=lambda q: q.when, reverse=True)

    def publishable(self):
        return self.first_round() and self.first_round().is_completed()

    def has_rounds(self):
        return len(self.rounds) > 0

    def has_adjudicators(self):
        return len(self.adjudicators) > 0

    def can_create_first_round(self):
        return all([self.has_adjudicators(), self.has_contestants(), not self.has_rounds(), self.equal_leads_follows(),
                    self.adjudicators_assigned()])

    def adjudicators_assigned(self):
        if self.floors > 1:
            return all([a.floor for a in self.adjudicator_assignments])
        return self.has_adjudicators()

    def has_contestants(self):
        if self.mode == CompetitionMode.single_partner:
            return len(self.couples) > 0
        else:
            return len(self.leads) > 0 and len(self.follows) > 0

    def equal_leads_follows(self):
        if self.mode != CompetitionMode.single_partner:
            return len(self.leads) == len(self.follows)
        else:
            return True

    def number_of_competitors(self):
        if self.mode == CompetitionMode.single_partner:
            return f"{len(self.couples)}"
        else:
            return f"{len(self.leads)}/{len(self.follows)}"

    def is_quali(self):
        return len(self.qualifications) > 0

    def is_quali_result(self):
        return self.qualification_id is not None

    def last_round_with_heat_list_published(self):
        rounds = [r for r in self.rounds if r.heat_list_published and r.type != RoundType.final]
        if len(rounds) > 0:
            return max(rounds, key=lambda x: x.round_id)
        return None

    def show_starting_list(self):
        if self.test:
            return False
        return True

    def starting_list_visible(self):
        if not self.show_starting_list():
            return False
        if self.is_quali_result():
            r = self.first_round()
            if r is None:
                return False
            else:
                return r.heat_list_published
        return True

    def starting_list_competitors(self):
        if self.is_single_partner():
            data = [{
                "couple_id": c.couple_id,
                "number": c.number,
                "team": c.team(),
                "lead": {"name": c.lead.name, "team": c.lead.team},
                "follow": {"name": c.follow.name, "team": c.follow.team},
            } for c in self.sorted_couples()]
            return data
        else:
            return {
                "leads": [d.json() for d in self.sorted_leads()],
                "follows": [d.json() for d in self.sorted_follows()],
            }

    def starting_list_data(self):
        return {
            "competition": self.starting_lists_json(),
            "competitors": self.starting_list_competitors(),
        }

    def show_result_list(self):
        return not self.test

    def sorted_couples(self):
        return list(sorted([c for c in self.couples], key=lambda c: c.number))

    def sorted_leads(self):
        return list(sorted([l for l in self.leads], key=lambda d: d.number))

    def sorted_follows(self):
        return list(sorted([f for f in self.follows], key=lambda d: d.number))

    def results_starting_list(self):
        if self.is_single_partner():
            return [c.starting_list_json() for c in self.sorted_couples()]
        elif self.is_random_single_partner():
            return [c.starting_list_json() for c in self.first_round().sorted_couples()]
        else:
            return {
                "leads": [d.json() for d in self.sorted_leads()],
                "follows": [d.json() for d in self.sorted_follows()],
            }

    def results(self):
        r = self.last_round()
        data = {
            "round": r.json(),
            "adjudicators": [a.json() for a in self.sorted_adjudicators()],
            "competitors": self.results_starting_list(),
            "evaluation_of_final": r.evaluation_of_final() if r.is_final() and r.is_completed() else None,
        }
        if self.is_change_per_dance():
            leads = r.ranking_report().json(LEAD)
            follows = r.ranking_report(follows=True).json(FOLLOW)
            data.update({
                "ranking_report": {
                    "leads": leads,
                    "follows": follows,
                },
                "competition_listing": {
                    "leads":  self.competition_listing(leads),
                    "follows":  self.competition_listing(follows),
                },
            })
        else:
            ranking_report = r.ranking_report().json()
            data.update({
                "ranking_report": ranking_report,
                "competition_listing": self.competition_listing(ranking_report),
            })
        return data

    def competition_listing(self, ranking_report):
        results = ranking_report["results"]
        rank = ranking_report["rank"]
        data = [{
            "round": r.presenter_json(),
            "results": [res for res in rank.values() if max(results[res["number"]]) == r.round_id]
        } for r in sorted([r for r in self.rounds], key=lambda x: x.round_id, reverse=True)]
        data = [r for r in data if len(r["results"]) > 0]
        return data

    def result(self, follows=False):
        return CompetitionResult(self, follows=follows)

    def max_couples(self):
        return max(len(self.couples), len(self.leads), len(self.follows))

    def generate_couples(self):
        if self.mode == CompetitionMode.single_partner:
            return self.couples
        else:
            follows = [d for d in self.follows]
            random.shuffle(follows)
            return generate_new_couples_from_dancers(self.leads, follows)

    def adjudicators_for_role(self, role=None):
        if role is not None:
            if role == LEAD:
                return [a for a in self.sorted_adjudicators() if a.assignment == AdjudicatorAssignmentEnum.lead
                        or a.assignment == AdjudicatorAssignmentEnum.both]
            else:
                return [a for a in self.sorted_adjudicators() if a.assignment == AdjudicatorAssignmentEnum.follow
                        or a.assignment == AdjudicatorAssignmentEnum.both]
        else:
            return self.sorted_adjudicators()

    def dancers(self):
        if self.is_single_partner():
            dancers = []
            for c in self.couples:
                dancers.append(c.lead)
                dancers.append(c.follow)
            return dancers
        return [d for d in self.leads + self.follows]

    def presenter_rounds(self):
        return [r.presenter_json() for r in self.rounds]

    def is_configurable(self):
        return True if self.first_round() is None else False
