from backend.models.base import db, TrackModifications, TABLE_ROUND
from .links import round_dance_table, round_couple_table
from .enums import RoundType, ROUND_SHORT_NAMES
from .constants import *
from backend.constants import FLOOR_MAP, LEAD, FOLLOW, ALL_ROLES
import random
from backend.models.competition.enums import CompetitionMode
from backend.models.couple import Couple
from backend.models.couple.functions import generate_new_couples_from_couples
from backend.models.heat import Heat
from backend.models.mark import Mark
from backend.models.couple_present import CouplePresent
from backend.models.round_result import RoundResult
from backend.models.final_placing import FinalPlacing
from backend.models.adjudicator_competition_assignment.enums import AdjudicatorAssignmentEnum
from backend.skating import generate_placings, SkatingSummary, RankingReport, TOTAL, RESULT
from itertools import combinations
import statistics


class Round(db.Model, TrackModifications):
    __tablename__ = TABLE_ROUND
    round_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(RoundType))
    min_marks = db.Column(db.Integer, default=1)
    max_marks = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=False)
    heat_list_published = db.Column(db.Boolean, default=False)
    competition_id = db.Column(db.Integer, db.ForeignKey("competition.competition_id",
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    competition = db.relationship("Competition", back_populates="rounds")
    dances = db.relationship("Dance", secondary=round_dance_table)
    couples = db.relationship("Couple", secondary=round_couple_table, back_populates="rounds")
    heats = db.relationship("Heat", back_populates="round", cascade="all, delete, delete-orphan")
    round_results = db.relationship("RoundResult", back_populates="round", cascade="all, delete, delete-orphan")
    dance_active = db.relationship("DanceActive", back_populates="round", cascade="all, delete, delete-orphan")
    final_placings = db.relationship("FinalPlacing", back_populates="round", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "{comp} {type}".format(comp=self.competition, type=self.type.value)

    def json(self):
        data = {
            "round_id": self.round_id,
            "name": self.type.value,
            "type": self.type.name,
            "number_of_couples": len(self.couples),
            "dances": [d.json() for d in self.sorted_active_dances()],
            "competition": {
                "competition_id": self.competition.competition_id,
                "name": self.competition.name(),
                "mode": self.competition.mode.name,
                "floors": self.competition.floors,
                "rounds": len(self.competition.rounds),
                "last_round_id": self.competition.last_round().round_id if self.competition.last_round() else 0,
                "discipline": self.competition.discipline_json(),
                "number_of_adjudicators": len(self.competition.adjudicators),
            },
            "completed": self.is_completed(),
            "mode": self.competition.mode.value,
            "first_dance": self.first_dance().json(),
            "floors": self.floors(),
            "number_of_floors": self.number_of_floors(),
            "min_marks": self.min_marks,
            "max_marks": self.max_marks,
            "target_marks": self.target_marks(),
            "is_active": self.is_active,
            "can_evaluate": self.can_evaluate(),
            "has_next_round": self.has_next_round(),
            "number_of_heats": self.number_of_heats(),
            "heat_list_published": self.heat_list_published,
            "is_split": self.is_split(),
        }
        # if self.single_partner_mode():
        #     data.update({
        #         "couples": [{
        #             "dancer_id": c.couple_id,
        #             "number": c.number,
        #             "lead": {"name": c.lead.name, "team": c.lead.team},
        #             "follow": {"name": c.follow.name, "team": c.follow.team},
        #         } for c in self.couples],
        #     })
        # else:
        #     pass
        return data

    def presenter_json(self):
        return {
            "round_id": self.round_id,
            "type": self.type.name,
            "name": self.type.value,
            "completed": self.is_completed(),
            "mode": self.competition.mode.name,
            "is_active": self.is_active,
            "floors": self.floors(),
         }

    def is_general_look(self):
        return self.type == RoundType.general_look

    def is_qualification(self):
        return self.type == RoundType.qualification

    def is_first_round(self):
        return self.type == RoundType.first_round

    def is_re_dance(self):
        return self.type == RoundType.re_dance

    def is_second_round(self):
        return self.type == RoundType.second_round

    def is_intermediate_round(self):
        return self.type == RoundType.intermediate_round

    def is_eight_final(self):
        return self.type == RoundType.eight_final

    def is_quarter_final(self):
        return self.type == RoundType.quarter_final

    def is_semi_final(self):
        return self.type == RoundType.semi_final

    def is_final(self):
        return self.type == RoundType.final

    def round_completed(self):
        return len(self.round_results) > 0

    def sorted_couples(self):
        return list(sorted(self.couples, key=lambda c: c.number))

    def sorted_adjudicators(self):
        return self.competition.sorted_adjudicators()

    def sorted_dances(self):
        return list(sorted(self.dances, key=lambda d: d.order))

    def first_dance(self):
        return self.sorted_dances()[0]

    def last_dance(self):
        return self.sorted_dances()[-1]

    def previous_dance(self, dance):
        try:
            return [d for d in self.sorted_dances() if d.order < dance.order][-1]
        except (IndexError, TypeError):
            return None

    def previous_dance_json(self, dance):
        try:
            return self.previous_dance(dance).json()
        except AttributeError:
            return None

    def next_dance(self, dance):
        try:
            return [d for d in self.sorted_dances() if d.order > dance.order][0]
        except (IndexError, TypeError):
            return None

    def next_dance_json(self, dance):
        try:
            return self.next_dance(dance).json()
        except AttributeError:
            return None

    def sorted_active_dances(self):
        return list(sorted(self.dance_active, key=lambda d: d.dance.order))

    def first_active_dance(self):
        dances = [d for d in self.sorted_active_dances() if d.is_active]
        return dances[0] if len(dances) > 0 else None

    def floors(self):
        return list(sorted(set([h.floor for h in self.heats])))

    def number_of_floors(self):
        return len(self.floors())

    def number_of_heats(self):
        return int(len(self.heats)/len(self.dances))

    def heat_numbers(self):
        return list(sorted(set([h.number for h in self.heats])))

    def is_completed(self):
        return len(self.round_results) > 0

    def deletable(self):
        return self.competition.last_round() == self

    def has_next_round(self):
        return any(r.round_id > self.round_id for r in self.competition.rounds)

    def set_marks(self, min_marks, max_marks=1):
        self.min_marks = min_marks
        self.max_marks = max(int(min_marks), int(max_marks))

    def target_marks(self):
        if self.min_marks == self.max_marks:
            return f"{self.min_marks}"
        else:
            return f"{self.min_marks}-{self.max_marks}"

    def progress_data(self):
        data = {"round": self.json()}
        if not self.is_completed():
            data.update({
                "competitors": self.competitors(),
                "data": self.couple_dance_heat_mapping(),
            })
        else:
            data.update({
                "data": self.results(),
                "cutoffs": self.cutoffs__html()
            })
        return data

    def competitors(self):
        if self.single_partner_mode() or self.competition.is_change_per_round():
            data = [c.starting_list_json() for c in self.sorted_couples()]
            return data
        else:
            return {
                "leads": [d.json() for d in self.leads()],
                "follows": [d.json() for d in self.follows()],
            }

    def single_partner_mode(self):
        return self.competition.is_single_partner() or self.competition.is_random_single_partner()

    def leads(self):
        return list(sorted([c.lead for c in self.couples], key=lambda d: d.number))

    def follows(self):
        return list(sorted([c.follow for c in self.couples], key=lambda d: d.number))

    def dancers(self):
        return self.leads() + self.follows()

    def couple_dance_heat_mapping(self):
        if self.competition.mode == CompetitionMode.single_partner \
                or self.competition.mode == CompetitionMode.random_single_partner:
            data = {d.dance_id: {c.number: None for c in self.couples} for d in self.dances}
            for h in self.heats:
                for c in h.couples:
                    data[h.dance_id][c.number] = h.heat_number()
            return data
        else:
            data = {d.dance_id: {d.number: None for d in self.dancers()} for d in self.dances}
            for h in self.heats:
                for c in h.couples:
                    data[h.dance_id][c.lead.number] = h.heat_number()
                    data[h.dance_id][c.follow.number] = h.heat_number()
            return data

    def is_dancer_in_competition(self, dancer):
        return dancer in self.competition.dancers()

    def couples_that_can_be_added(self):
        numbers = [d.number for d in self.competition.dancers()]
        return Couple.query.filter(Couple.number.notin_(numbers)).all()

    def add_couple(self, couple):
        if not self.is_dancer_in_competition(couple.lead) and not self.is_dancer_in_competition(couple.follow):
            if self.competition.is_single_partner():
                self.competition.couples.append(couple)
            elif self.competition.is_random_single_partner() or self.competition.is_change_per_round():
                self.competition.leads.append(couple.lead)
                self.competition.follows.append(couple.follow)
            self.couples.append(couple)
            for dance in self.dances:
                heats = sorted([h for h in self.heats if h.dance == dance], key=lambda x: len(x.couples))
                heat = heats[0]
                cp = CouplePresent()
                cp.couple = couple
                cp.heat = heat
                heat.couples.append(couple)
                for adj in self.competition.adjudicators:
                    m = Mark()
                    m.adjudicator = adj
                    m.couple = couple
                    m.heat = heat
            db.session.commit()

    def remove_couple(self, couple):
        if self.competition.is_single_partner():
            self.competition.couples.remove(couple)
        elif self.competition.is_random_single_partner() or self.competition.is_change_per_round():
            self.competition.leads.remove(couple.lead)
            self.competition.follows.remove(couple.follow)
        self.couples.remove(couple)
        couples_present = CouplePresent.query.filter(CouplePresent.heat_id.in_([h.heat_id for h in self.heats]),
                                                     CouplePresent.couple == couple).all()
        for cp in couples_present:
            cp.heat.couples.remove(couple)
            db.session.delete(cp)
        Mark.query.filter(Mark.heat_id.in_([h.heat_id for h in self.heats]),
                          Mark.couple == couple).delete(synchronize_session="fetch")
        db.session.commit()

    def results(self):
        return [r.json() for r in self.sorted_results() if r.marks == -1] + \
               [r.json() for r in self.sorted_results() if r.marks != -1]

    def sorted_results(self):
        if self.is_final():
            return list(sorted(self.round_results, key=lambda r: (r.follow, r.final_placing)))
        else:
            return list(sorted(self.round_results, key=lambda r: (r.marks, not r.follow), reverse=True))

    def cutoffs(self):
        if self.competition.is_change_per_dance():
            results = [r for r in self.round_results if r.marks > 0]
            round_result_list = sorted([r.marks for r in results])
            unique_results = list(set(round_result_list))
            unique_results.sort(reverse=True)
            viable_unique_results = []
            for r in unique_results:
                matching_results = [result for result in results if result.marks >= r]
                leads = [result for result in matching_results if not result.follow]
                follows = [result for result in matching_results if result.follow]
                if len(leads) == len(follows):
                    viable_unique_results.append(r)
            unique_results = viable_unique_results
        else:
            round_result_list = sorted([r.marks for r in self.round_results if r.marks > 0])
            unique_results = list(set(round_result_list))
            unique_results.sort(reverse=True)
        return unique_results

    def cutoffs__html(self):
        cutoffs = [-1] + self.cutoffs()
        return [{"value": r, "text": r} for r in cutoffs]

    def can_evaluate(self):
        if self.is_final():
            for adjudicator in self.competition.adjudicators:
                for dance in self.dances:
                    placings = [p for p in self.final_placings if p.adjudicator == adjudicator and p.dance == dance]
                    results = [p.final_placing for p in placings]
                    if len(set(results)) != len(placings) or 0 in results:
                        return False
        else:
            for adjudicator in self.competition.adjudicators:
                for dance in self.dances:
                    marks = [m.mark for m in self.adjudicator_marks(adjudicator, dance) if m.mark]
                    if True not in marks:
                        return False
        return True

    def count_mark_mapping(self):
        adj_enum = AdjudicatorAssignmentEnum
        enum_map = {
            LEAD: {adj_enum.lead: True, adj_enum.follow: False, adj_enum.both: True},
            FOLLOW: {adj_enum.lead: False, adj_enum.follow: True, adj_enum.both: True},
        }
        return {
            role: {
                a.adjudicator: enum_map[role][a.assignment] for a in self.sorted_adjudicators()
            } for role in ALL_ROLES
        }

    def generate_final_results(self, follows=False):
        skating = self.skating_summary(follows=follows)
        summary = skating.summary
        for couple in skating.couples.values():
            result = RoundResult()
            result.round = self
            result.follow = follows
            result.couple = skating.reference_couples[couple]
            result.total = summary[TOTAL][couple].item()
            result.final_placing = summary[RESULT][couple].item()

    def evaluate(self):
        if self.is_final():
            self.generate_final_results()
            if self.competition.is_change_per_dance():
                self.generate_final_results(follows=True)
            db.session.commit()
        elif not self.is_general_look():
            if self.competition.is_change_per_dance():
                count_mark = self.count_mark_mapping()
                dancers = self.dancers()
                dancer_marks = {d: 0 for d in dancers}
                for dancer in dancers:
                    marks = [mark for heat in self.heats for mark in heat.marks
                             if mark.couple.lead == dancer or mark.couple.follow == dancer]
                    for mark in marks:
                        if mark.mark:
                            if count_mark[dancer.role][mark.adjudicator]:
                                dancer_marks[dancer] += 1
                dancer_couple_map = {c.lead: c for c in self.couples}
                dancer_couple_map.update({c.follow: c for c in self.couples})
                previous_round = self.previous_round()
                if self.type == RoundType.re_dance:
                    max_marks = max(dancer_marks.values()) + 1
                    direct_qualified_leads = {c.lead: c for c in previous_round.couples if c.lead not in dancers}
                    direct_qualified_follows = {c.follow: c for c in previous_round.couples if c.follow not in dancers}
                    dancer_marks.update({d: max_marks for d in direct_qualified_leads.keys()})
                    dancer_marks.update({d: max_marks for d in direct_qualified_follows.keys()})
                    dancer_couple_map.update({d: direct_qualified_leads[d] for d in direct_qualified_leads.keys()})
                    dancer_couple_map.update({d: direct_qualified_follows[d] for d in direct_qualified_follows.keys()})
                for dancer, marks in dancer_marks.items():
                    result = RoundResult()
                    result.couple = dancer_couple_map[dancer]
                    result.marks = marks
                    result.round = self
                    result.follow = dancer.role == FOLLOW
            else:
                couples = self.couples
                couple_marks = {c: 0 for c in couples}
                for couple in couples:
                    marks = [mark for heat in self.heats for mark in heat.marks if mark.couple == couple]
                    for mark in marks:
                        if mark.mark:
                            couple_marks[couple] += 1
                previous_round = self.previous_round()
                if self.type == RoundType.re_dance:
                    max_marks = max(couple_marks.values()) + 1
                    direct_qualified_couples = [c for c in previous_round.couples if c.number
                                                not in [c.number for c in couples]]
                    couple_marks.update({couple: max_marks for couple in direct_qualified_couples})
                for couple, marks in couple_marks.items():
                    result = RoundResult()
                    result.couple = couple
                    result.marks = marks
                    result.round = self
            round_result_list = [r.marks for r in self.round_results]
            result_map = generate_placings(round_result_list)
            for result in self.round_results:
                result.placing = result_map[result.marks]
            if self.type == RoundType.re_dance:
                max_marks = max([r.marks for r in self.round_results])
                for result in self.round_results:
                    if result.marks == max_marks:
                        result.marks = -1
            db.session.commit()

    def create_heats(self, heats, floors=1, different_heats=False):
        couples = [c for c in self.couples]
        if self.competition.is_change_per_dance():
            random.shuffle(couples)
            for idx, dance in enumerate(self.dances):
                couples = generate_new_couples_from_couples(couples, offset=idx)
                couples_split = self.split_couples_into_heats(couples, heats, floors)
                self.generate_heats(couples_split, dance, floors)
        else:
            couples_split = self.split_couples_into_heats(couples, heats, floors)
            for dance in self.dances:
                if different_heats:
                    couples_split = self.split_couples_into_heats(couples, heats, floors)
                self.generate_heats(couples_split, dance, floors)
        db.session.commit()

    def generate_heats(self, couples_split, dance, floors):
        for idx, c in enumerate(couples_split):
            heat = Heat()
            if floors > 1:
                heat.floor = FLOOR_MAP[idx % floors]
            heat.dance = dance
            heat.couples = c
            heat.number = int(idx / floors) + 1
            self.heats.append(heat)
            for couple in c:
                present = CouplePresent()
                present.couple = couple
                present.present = False
                heat.couples_present.append(present)
                for adj in self.competition.adjudicators:
                    mark = Mark()
                    mark.adjudicator = adj
                    mark.couple = couple
                    heat.marks.append(mark)

    @staticmethod
    def split_couples_into_heats(couples, heats, floors=1):
        n = len(couples)
        k = heats * floors
        random.shuffle(couples)
        return [couples[i * (n // k) + min(i, n % k):(i + 1) * (n // k) + min(i + 1, n % k)] for i in range(k)]

    def create_final(self):
        couples = [c for c in self.couples]
        if self.competition.is_change_per_dance():
            random.shuffle(couples)
            for idx, dance in enumerate(self.dances):
                couples = generate_new_couples_from_couples(couples, offset=1)
                self.generate_final_placings(self.competition.adjudicators, couples, dance)
        else:
            if self.competition.is_change_per_round():
                couples = generate_new_couples_from_couples(couples, offset=random.randrange(1, len(couples) + 1))
            for dance in self.dances:
                self.generate_final_placings(self.competition.adjudicators, couples, dance)
        db.session.commit()

    def generate_final_placings(self, adjudicators, couples, dance):
        heat = Heat()
        heat.dance = dance
        heat.couples = couples
        heat.round = self
        for adj in adjudicators:
            for couple in couples:
                final_placing = FinalPlacing()
                final_placing.adjudicator = adj
                final_placing.couple = couple
                final_placing.dance = dance
                self.final_placings.append(final_placing)

    def split_options(self):
        splits = list(sorted([c for c in self.cutoffs()], reverse=True))
        splittings = [s for s in combinations(splits, len(self.competition.qualifications) - 1)]
        split_counter = {s: [] for s in splittings}
        if self.competition.is_change_per_dance():
            for s in splittings:
                results = self.sorted_results()
                for idx, split, in enumerate(s):
                    split_counter[s].append(len([r for r in results if r.marks >= split]))
                    results = [r for r in results if r.marks < split]
                split_counter[s].append(len(results))
        else:
            for s in splittings:
                results = self.sorted_results()
                for idx, split, in enumerate(s):
                    split_counter[s].append(len([r.couple for r in results if r.marks >= split]))
                    results = [r for r in results if r.marks < split]
                split_counter[s].append(len(results))
        splittings.sort(key=lambda s: statistics.stdev(split_counter[s]))
        return {s: split_counter[s] for s in splittings}

    def split_options__html(self):
        splits = {
            " / ".join([str(s) for s in v]): "-".join([str(s) for s in k]) for k, v in self.split_options().items()
        }
        return [{"value": v, "text": k} for k, v in splits.items()]

    def split_qualification(self, split_option):
        split_option = [int(s) for s in split_option.split("-")]
        competitions = self.competition.sorted_qualifications()
        if self.competition.is_change_per_dance():
            results = self.sorted_results()
            for idx, split, in enumerate(split_option):
                couples = [r for r in results if r.marks >= split]
                competitions[idx].leads = [r.couple.lead for r in couples if not r.follow]
                competitions[idx].follows = [r.couple.follow for r in couples if r.follow]
                results = [r for r in results if r.marks < split]
            competitions[-1].leads = [r.couple.lead for r in results if not r.follow]
            competitions[-1].follows = [r.couple.follow for r in results if r.follow]
        else:
            results = self.sorted_results()
            for idx, split, in enumerate(split_option):
                couples = [r.couple for r in results if r.marks >= split]
                if competitions[idx].is_single_partner():
                    competitions[idx].couples = couples
                else:
                    competitions[idx].leads = [c.lead for c in couples]
                    competitions[idx].follows = [c.follow for c in couples]
                results = [r for r in results if r.marks < split]
            couples = [r.couple for r in results]
            if competitions[-1].is_single_partner():
                competitions[-1].couples = couples
            else:
                competitions[-1].leads = [c.lead for c in couples]
                competitions[-1].follows = [c.follow for c in couples]
        db.session.commit()

    def is_split(self):
        return sum([len(c.couples + c.leads + c.follows) for c in [q for q in self.competition.qualifications]]) > 0

    def reports_data(self):
        data = {"round": self.json()}
        reports = []
        if self.number_of_heats() > 1 or self.competition.is_change_per_dance():
            reports.append(HEATS_BY_STARTING_NUMBER)
            reports.append(HEATS_BY_DANCE)
        reports.append(QUALIFIED_STARTS)
        if self.is_re_dance():
            reports.append(NO_RE_DANCE)
        if not self.is_general_look():
            reports.append(ADJUDICATORS)
            reports.append(ADJUDICATION_SHEETS)
        if self.is_completed():
            if not self.is_final():
                reports.append(PLACINGS_AFTER_ROUND)
            if self.is_final():
                reports.append(EVALUATION_OF_FINAL)
                # reports.append(COMPETITION_RESULT)
                reports.append(RANKING_REPORT)
        data.update({
            "data": reports,
        })
        return data

    def printing_data(self, prints):
        data = {}
        if any(p in [HEATS_BY_STARTING_NUMBER, HEATS_BY_DANCE, QUALIFIED_STARTS, NO_RE_DANCE] for p in prints):
            data.update({
                "competitors": self.competitors()
            })
        for p in prints:
            if p == HEATS_BY_STARTING_NUMBER:
                data.update({
                    HEATS_BY_STARTING_NUMBER: {
                        "heat_mapping": self.couple_dance_heat_mapping(),
                        "partner_mapping": self.lead_follow_mapping() if self.competition.is_change_per_dance() else {}
                    }
                })
            if p == HEATS_BY_DANCE:
                data.update({
                    HEATS_BY_DANCE: {
                        "heat_mapping": self.heat_dance_mapping(),
                        "partner_mapping": self.lead_follow_mapping() if self.competition.is_change_per_dance() else {}
                    }
                })
            if p == NO_RE_DANCE:
                data.update({
                    NO_RE_DANCE: self.no_re_dance_couples()
                })
            if p == ADJUDICATORS:
                data.update({
                    ADJUDICATORS: [a.json() for a in self.competition.sorted_adjudicators()]
                })
            if p == ADJUDICATION_SHEETS:
                data.update({
                    ADJUDICATION_SHEETS: {
                        "adjudicators": [a.json() for a in self.competition.sorted_adjudicators()],
                        "mapping": self.adjudication_sheet_mapping()
                    }
                })
            if p == PLACINGS_AFTER_ROUND:
                data.update({
                    PLACINGS_AFTER_ROUND: {
                        "this_round": self.results(),
                        "previous_rounds": self.results_previous_rounds(),
                    }
                })
            if p == EVALUATION_OF_FINAL:
                data.update({
                    EVALUATION_OF_FINAL: self.evaluation_of_final()
                })
            if p == COMPETITION_RESULT:
                data.update({
                    COMPETITION_RESULT: []
                })
            if p == RANKING_REPORT:
                if self.competition.is_change_per_dance():
                    data.update({
                        RANKING_REPORT: {
                            "leads": self.ranking_report().json(LEAD),
                            "follows": self.ranking_report(follows=True).json(FOLLOW),
                        }
                    })
                else:
                    data.update({
                        RANKING_REPORT: self.ranking_report().json()
                    })
        return data

    def heat_dance_mapping(self):
        if self.competition.is_change_per_dance():
            return {
                d.dance_id: {
                    h.heat_number(): [
                        d.json() for d in h.ordered_dancers()
                    ] for h in self.heats if h.dance_id == d.dance_id
                } for d in self.sorted_active_dances()
            }
        else:
            return {
                d.dance_id: {
                    h.heat_number(): [
                        c.json() for c in h.ordered_couples_present()
                    ] for h in self.heats if h.dance_id == d.dance_id
                } for d in self.sorted_active_dances()
            }

    def lead_follow_mapping(self):
        lead_follow_map = {d.dance_id: {} for d in self.dances}
        for dance in self.dances:
            heats = [heat for heat in self.heats if heat.dance == dance]
            lead_follow = {couple.number: couple.follow.number for heat in heats for couple in heat.couples}
            follow_lead = {couple.follow.number: couple.number for heat in heats for couple in heat.couples}
            lead_follow_map[dance.dance_id].update(lead_follow)
            lead_follow_map[dance.dance_id].update(follow_lead)
        return lead_follow_map

    def no_re_dance_couples(self):
        previous_round = self.previous_round()
        if self.competition.is_change_per():
            return {
                "leads": [d.json() for d in previous_round.leads() if d not in self.leads()],
                "follows": [d.json() for d in previous_round.follows() if d not in self.follows()],
            }
        else:
            return [c.starting_list_json() for c in previous_round.sorted_couples() if c not in self.couples]

    def adjudication_sheet_mapping(self):
        if self.is_final():
            return {
                a.adjudicator_id: {
                    d.dance_id:  [
                        p.json() for p in self.ordered_final_placings(dance_id=d.dance_id, adjudicator=a.adjudicator)
                    ] for d in self.sorted_active_dances()
                } for a in self.competition.sorted_adjudicators()
            }
        return {
            a.adjudicator_id: {
                d.dance_id: {
                    h.heat_number(): [
                        c.json() for c in h.ordered_marks(a.adjudicator)
                    ] for h in self.heats if h.dance_id == d.dance_id and (h.floor == a.floor or h.floor is None)
                } for d in self.sorted_active_dances()
            } for a in self.competition.sorted_adjudicators()
        }

    def results_previous_rounds(self):
        if self.competition.first_round() == self or self.is_re_dance():
            return []
        this_round_results = self.results()
        results = self.competition.first_round().results()
        for r in self.competition.rounds:
            if r.round_id < self.round_id:
                next_results = r.results()
                results[0:len(next_results)] = next_results
        return results[len(this_round_results)-len(results):]

    def final_evaluation_data(self, follows=False):
        skating = self.skating_summary(follows=follows)
        data = {
            "summary": [[c for c in r] for r in skating.summary.itertuples()],
        }
        data.update({
            "rule10": [[str(c) for c in r] for r in skating.summary_rule_10.skating.itertuples()]
            if skating.show_rule_10 or skating.show_rule_11 else [],
            "rule11": [[str(c) for c in r] for r in
                       skating.summary_rule_11.skating.itertuples()] if skating.show_rule_11 else [],
        })
        if self.competition.is_change_per_dance():
            adjudicators = self.adjudicators_for_role(FOLLOW if follows else LEAD)
        else:
            adjudicators = self.adjudicators_for_role()
        data.update({
            "adjudicators": [{
                "adjudicator_id": a.adjudicator.adjudicator_id,
                "name": a.adjudicator.name,
                "tag": a.adjudicator.tag,
            } for a in list(sorted(adjudicators, key=lambda a: a.adjudicator.tag))],
            "dances": {
                d.dance_id: [
                    [str(c) for c in r] for r in skating.skating_dances[d].skating.itertuples()
                ] for d in skating.skating_dances
            },
        })
        if self.competition.is_change_per_dance():
            if follows:
                data.update({
                    "numbers": {c.follow.number: c.follow.name for c in skating.reference_couples.values()}
                })
            else:
                data.update({
                    "numbers": {c.lead.number: c.lead.name for c in skating.reference_couples.values()}
                })
        else:
            data.update({
                "numbers": {c.number: c.names() for c in skating.reference_couples.values()}
            })
        return data

    def evaluation_of_final(self):
        data = self.final_evaluation_data()
        if self.competition.is_change_per():
            data.update({"follows": self.final_evaluation_data(follows=True)})
        return data

    def floor_management_data(self, dance_id):
        data = {
            "couples": [c.json() for h in self.heats for c in h.couples_present if h.dance_id == dance_id]
        }
        if len(self.floors()) > 1:
            data.update({
                "mapping": {
                    number: {
                        h.floor: [
                            c.json() for c in h.ordered_couples_present()
                        ] for h in self.heats if h.number == number and h.dance_id == dance_id
                    } for number in self.heat_numbers()
                }
            })
        else:
            data.update({
                "mapping": {
                    h.number: [
                        c.json() for c in h.ordered_couples_present()
                    ] for h in self.heats if h.dance_id == dance_id
                }
            })
        return data

    def ordered_final_placings(self, dance_id=None, adjudicator=None):
        placings = [p for p in self.final_placings if p.dance_id == dance_id] if dance_id else self.final_placings
        if adjudicator:
            placings = [p for p in placings if p.adjudicator == adjudicator]
        return list(sorted(placings, key=lambda c: c.couple.number))

    def ordered_marks(self, dance_id=None, adjudicator=None):
        marks = []
        if dance_id is None and adjudicator is None:
            marks = [m for h in self.heats for m in h.marks]
        if dance_id is not None and adjudicator is None:
            marks = [m for h in self.heats for m in h.marks if h.dance_id == dance_id]
        if dance_id is None and adjudicator is not None:
            marks = [m for h in self.heats for m in h.marks
                     if m.adjudicator == adjudicator.adjudicator and (h.floor == adjudicator.floor or h.floor is None)]
        if dance_id is not None and adjudicator is not None:
            marks = [m for h in self.heats for m in h.marks if h.dance_id == dance_id
                     and m.adjudicator == adjudicator.adjudicator and (h.floor == adjudicator.floor or h.floor is None)]
        return list(sorted(marks, key=lambda c: c.couple.number))

    def save_placings(self, placings, dance_id):
        placings = {p["final_placing_id"]: p["final_placing"] for p in placings}
        for placing in self.ordered_final_placings(dance_id):
            placing.final_placing = placings[placing.final_placing_id]
        db.session.commit()

    def move_couple_data(self, dance_id):
        return [{
            "heat": h.json(),
            "couples": [c.json() for c in h.ordered_couples_present()]
        } for h in self.heats if h.dance_id == dance_id]

    def adjudication_data(self, dance_id, dancing_round=False):
        data = {}
        if self.is_final():
            data.update({
                "mapping": {
                    a.adjudicator_id: {
                        "adjudicator": a.adjudication_json(dancing_round=self, dance_id=dance_id),
                        "placings": [
                            p.json() for p in self.ordered_final_placings(dance_id=dance_id, adjudicator=a.adjudicator)
                        ]
                    } for a in self.sorted_adjudicators()
                },
                "couples": [p.json() for p in self.ordered_final_placings(dance_id=dance_id)],
            })
        else:
            data.update({
                "mapping": {
                    a.adjudicator_id: {
                        "adjudicator": a.adjudication_json(dancing_round=self, dance_id=dance_id),
                        "marks": [m.json() for m in self.ordered_marks(dance_id=dance_id, adjudicator=a)]
                    } for a in self.sorted_adjudicators()
                },
                "couples": [m.json() for m in self.ordered_marks(dance_id=dance_id)],
            })
        if dancing_round:
            data.update({
                "round": self.json()
            })
        return data

    def toggle_active_dances(self):
        self.is_active = not self.is_active
        for dance in self.dance_active:
            dance.is_active = self.is_active
        db.session.commit()

    def toggle_active_dance(self, dance_id):
        self.is_active = True
        for dance in self.dance_active:
            if dance.dance_id == dance_id:
                dance.is_active = not dance.is_active
        db.session.commit()

    def deactivate(self):
        for dance in self.dance_active:
            dance.is_active = False
        self.is_active = False
        db.session.commit()

    def short_name(self):
        return ROUND_SHORT_NAMES[self.type]

    def is_published(self):
        if self.competition.heat_list is None:
            return False
        return self.__repr__() in self.competition.heat_list

    def final_completed(self):
        placings = list(range(1, len(self.couples) + 1))
        for dance in self.dances:
            for adjudicator in self.competition.adjudicators:
                adjudicator_placings = \
                    sorted([final_placing.final_placing for final_placing in self.final_placings
                            if final_placing.adjudicator == adjudicator and final_placing.dance == dance
                            and final_placing.final_placing is not None])
                if placings != adjudicator_placings:
                    return False
        return not self.is_active

    def presenter_final_results(self):
        skating = self.skating_summary()
        data = {
            "summary": [[c for c in r] for r in skating.summary.itertuples()],
        }
        data.update({
            "rule10": [[str(c) for c in r] for r in
                       skating.summary_rule_10.skating.itertuples()] if skating.show_rule_10 else [],
            "rule11": [[str(c) for c in r] for r in
                       skating.summary_rule_11.skating.itertuples()] if skating.show_rule_11 else [],
        })
        if self.competition.is_change_per_dance():
            skating = self.skating_summary(follows=True)
            follows_data = {
                "summary": [[c for c in r] for r in skating.summary.itertuples()],
            }
            follows_data.update({
                "rule10": [[str(c) for c in r] for r in
                           skating.summary_rule_10.skating.itertuples()] if skating.show_rule_10 else [],
                "rule11": [[str(c) for c in r] for r in
                           skating.summary_rule_11.skating.itertuples()] if skating.show_rule_11 else [],
            })
            data.update({
                "follows": follows_data
            })
        return data

    def presenter_adjudicators(self):
        return [{
            "adjudicator_id": a.adjudicator.adjudicator_id,
            "name": a.adjudicator.name,
            "present": a.adjudicator.is_present(self),
            "round": a.adjudicator.active_round(),
            "dance": a.adjudicator.active_dance(),
            "floor": a.floor,
        } for a in self.competition.sorted_adjudicators()]

    def starting_list(self):
        if self.single_partner_mode() or self.competition.is_change_per_round():
            return [c.presenter_json() for c in self.sorted_couples()]
        return {
            "leads": [d.json() for d in self.leads()],
            "follows": [d.json() for d in self.follows()],
        }

    def couples_present(self):
        return {
            "round": self.presenter_json(),
            "dances": [d.json() for d in self.sorted_dances()],
            "heat_mapping": self.heat_dance_mapping(),
            "partner_mapping": self.lead_follow_mapping() if self.competition.is_change_per_dance() else {}
        }

    def previous_round(self):
        previous_rounds = [r.round_id for r in self.competition.rounds if r.round_id < self.round_id]
        try:
            previous_rounds = [r for r in self.competition.rounds if r.round_id == max(previous_rounds)]
        except ValueError:
            return None
        else:
            return previous_rounds[0]

    def adjudicators_for_role(self, role=None):
        return self.competition.adjudicators_for_role(role)

    def has_dance(self, dance_id):
        return dance_id in [d.dance_id for d in self.dances]

    def is_dance_active(self, dance):
        return [d for d in self.dance_active if d.dance == dance][0].is_active

    def adjudicator_marks(self, adjudicator, dance):
        marks = []
        for heat in self.heats:
            if heat.dance == dance:
                marks.extend([m for m in heat.marks if m.adjudicator == adjudicator])
        marks.sort(key=lambda x: x.couple.number)
        return marks

    def skating_summary(self, follows=False):
        return SkatingSummary(dancing_round=self, follows=follows)

    def ranking_report(self, follows=False):
        return RankingReport(self.competition, follows=follows)

    def marks(self, dance=None):
        if dance is not None:
            return [mark for heat in self.heats for mark in heat.marks if heat.dance == dance]
        else:
            return [mark for heat in self.heats for mark in heat.marks]
