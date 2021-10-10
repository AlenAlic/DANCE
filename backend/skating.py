import pandas
import math
from contextlib import suppress
from backend.constants import LEAD, FOLLOW


RESULT = "Result"
TOTAL = "Total"
QUALIFIED = "Qualified"
FIRST = "First"
SUM = "Sum"


class SkatingDance:
    def __init__(self, dancing_round=None, dance=None, follows=False):
        if dancing_round is not None and dance is not None:
            self.placing_columns = list(range(1, len(dancing_round.couples) + 1))
            if dancing_round.competition.is_change_per_dance():
                self.adjudicators = dancing_round.adjudicators_for_role(FOLLOW if follows else LEAD)
            else:
                self.adjudicators = dancing_round.sorted_adjudicators()
            self.adjudicator_columns = sorted([a.adjudicator.tag for a in self.adjudicators])
            self.majority = math.ceil(len(self.adjudicator_columns) / 2)
            columns = self.adjudicator_columns + self.placing_columns + [RESULT]
            if follows:
                for heat in [heat for heat in dancing_round.heats if heat.dance == dance]:
                    self.couples = {c.number: c.follow.number for c in
                                    sorted([c for c in heat.couples], key=lambda x: x.follow.number)}
            else:
                self.couples = {num: num for num in sorted([c.number for c in dancing_round.couples])}
            self.dance = dance.tag
            self.skating = pandas.DataFrame(index=self.couples.values(), columns=columns)
            for a in [a.adjudicator for a in self.adjudicators]:
                for placing in [p for p in dancing_round.final_placings if p.dance == dance and p.adjudicator == a]:
                    self.skating.loc[self.couples[placing.couple.number],
                                     placing.adjudicator.tag] = placing.final_placing
            self.apply_rules()

    def apply_rules(self):
        self.skating[RESULT] = [0 for _ in self.couples]
        for col in self.placing_columns:
            for couple in self.couples.values():
                count = 0
                for adj in self.adjudicator_columns:
                    if self.skating.loc[couple, adj] <= col:
                        count += 1
                if self.skating.loc[couple, RESULT] == 0:
                    self.skating.loc[couple, col] = count
                else:
                    self.skating.loc[couple, col] = 0
        for col in self.placing_columns:
            self.rule_5(col)

    def rule_5(self, col, couples=None, placings=None):
        if couples is None:
            couples = self.couples.values()
        majority_couples = [couple for couple in couples if self.skating.loc[couple, RESULT] == 0]
        majority_couples = [couple for couple in majority_couples if self.skating.loc[couple, col] >= self.majority
                            and self.skating.loc[couple, RESULT] == 0]
        if placings is None:
            obtained_placings = [n for n in self.skating[RESULT].values if n > 0]
            placings = list(range(len(obtained_placings) + 1, len(obtained_placings) + 1 + len(majority_couples)))
        if len(majority_couples) == 1:
            if self.skating.loc[majority_couples[0], RESULT] == 0:
                self.skating.loc[majority_couples[0], RESULT] = min(placings)
                placings.remove(min(placings))
                if col + 1 in self.placing_columns:
                    marked_out_columns = [c for c in self.placing_columns if c >= col + 1]
                    for moc in marked_out_columns:
                        self.skating.loc[majority_couples[0], moc] = "-"
        elif len(majority_couples) > 1:
            self.rule_6(col, majority_couples, placings)

    def rule_6(self, col, majority_couples, placings):
        rule_6_couples = {couple: self.skating.loc[couple, col] for couple in majority_couples}
        split_couples = [{couple: self.skating.loc[couple, col] for couple in majority_couples
                          if self.skating.loc[couple, col] == c}
                         for c in sorted(set(rule_6_couples.values()), reverse=True)]
        for couples in split_couples:
            greater_majority = max([self.skating.loc[c, col] for c in majority_couples
                                    if self.skating.loc[c, RESULT] == 0])
            if list(couples.values()).count(greater_majority) == 1:
                for c in couples:
                    if self.skating.loc[c, col] == greater_majority:
                        self.skating.loc[c, RESULT] = min(placings)
                        placings.remove(min(placings))
                        if col + 1 in self.placing_columns:
                            marked_out_columns = [c for c in self.placing_columns if c >= col + 1]
                            for moc in marked_out_columns:
                                self.skating.loc[c, moc] = "-"
                        break
            elif len(couples) > 0:
                self.rule_7(col, [c for c in couples], placings[:len(couples)])
                placings = placings[len(couples):]

    def rule_7(self, col, majority_couples, placings):
        rule_7_couples = {couple: sum([self.skating.loc[couple, adj] for adj in self.adjudicator_columns
                                       if self.skating.loc[couple, adj] <= col]) for couple in majority_couples}
        split_couples = [{couple: sum([self.skating.loc[couple, adj] for adj in self.adjudicator_columns
                                       if self.skating.loc[couple, adj] <= col]) for couple in majority_couples
                          if sum([self.skating.loc[couple, adj] for adj in self.adjudicator_columns
                                  if self.skating.loc[couple, adj] <= col]) == c}
                         for c in sorted(set(rule_7_couples.values()))]
        for couples in split_couples:
            min_place_marks = min(list(couples.values()))
            if list(couples.values()).count(min_place_marks) == 1:
                for c in couples:
                    if couples[c] == min_place_marks:
                        self.skating.loc[c, col] = f"{self.skating.loc[c, col]}({rule_7_couples[c]})"
                        self.skating.loc[c, RESULT] = min(placings)
                        placings.remove(min(placings))
                        del couples[c]
                        if col + 1 in self.placing_columns:
                            marked_out_columns = [c for c in self.placing_columns if c >= col + 1]
                            for moc in marked_out_columns:
                                self.skating.loc[c, moc] = "-"
                        break
                if len(couples) > 0:
                    self.rule_6(col, [c for c in couples], placings[:len(couples)])
                    placings = placings[len(couples):]
            elif len(couples) > 0:
                for c in couples:
                    self.skating.loc[c, col] = f"{self.skating.loc[c, col]}({couples[c]})"
                # Rule 8
                if col + 1 in self.placing_columns:
                    self.rule_5(col + 1, [c for c in couples], placings[:len(couples)])
                    placings = placings[len(couples):]
                else:
                    final_placing = sum(placings) / len(placings)
                    for c in majority_couples:
                        self.skating.loc[c, RESULT] = final_placing


class Rule10(SkatingDance):
    def __init__(self, dancing_round, follows=False):
        super().__init__()
        self.placing_columns = list(range(1, len(dancing_round.couples) + 1))
        columns = self.placing_columns + [RESULT]
        if follows:
            self.couples = {c.number: c.follow.number for c in
                            sorted([c for c in dancing_round.couples], key=lambda x: x.follow.number)}
        else:
            self.couples = {num: num for num in sorted([c.number for c in dancing_round.couples])}
        self.skating = pandas.DataFrame(index=self.couples.values(), columns=columns)
        self.skating = self.skating.fillna("")

    def apply_rules(self):
        pass

    def rule_5(self, col, couples=None, placings=None):
        pass

    def rule_6(self, col, majority_couples, placings):
        pass

    def rule_7(self, col, majority_couples, placings):
        pass


class Rule11(SkatingDance):
    def __init__(self, dancing_round, follows=False):
        super().__init__()
        self.follows = follows
        self.dancing_round = dancing_round
        self.placing_columns = list(range(1, len(dancing_round.couples) + 1))
        self.adjudicator_columns = [d.tag + "-" + adj for d in dancing_round.dances
                                    for adj in sorted([adj.tag for adj in dancing_round.competition.adjudicators])]
        self.majority = math.ceil(len(self.adjudicator_columns) / 2)
        columns = self.adjudicator_columns + self.placing_columns + [RESULT]
        if follows:
            self.couples = {c.number: c.follow.number for c in
                            sorted([c for c in dancing_round.couples], key=lambda x: x.follow.number)}
        else:
            self.couples = {num: num for num in sorted([c.number for c in dancing_round.couples])}
        self.skating = pandas.DataFrame(index=self.couples.values(), columns=columns)

    def apply_rules(self):
        pass

    def rule_5(self, col, couples=None, placings=None):
        if couples is None:
            couples = self.couples.values()
        majority_couples = [couple for couple in couples if self.skating.loc[couple, RESULT] == 0]
        majority_couples = [couple for couple in majority_couples if self.skating.loc[couple, col] >= self.majority
                            and self.skating.loc[couple, RESULT] == 0]
        if len(majority_couples) == 0:
            if col + 1 in self.placing_columns:
                self.rule_5(col+1, couples)
        if placings is None:
            obtained_placings = [n for n in self.skating[RESULT].values if n > 0]
            placings = list(range(len(obtained_placings) + 1, len(obtained_placings) + 1 + len(majority_couples)))
        # Rule 5
        if len(majority_couples) == 1:
            if self.skating.loc[majority_couples[0], RESULT] == 0:
                self.skating.loc[majority_couples[0], RESULT] = min(placings)
                placings.remove(min(placings))
                couples.remove(majority_couples[0])
                if col + 1 in self.placing_columns:
                    marked_out_columns = [c for c in self.placing_columns if c >= col + 1]
                    for moc in marked_out_columns:
                        self.skating.loc[majority_couples[0], moc] = 0
                self.rule_5(col, couples)
        elif len(majority_couples) > 1:
            self.rule_6(col, majority_couples, placings)

    def populate(self, place, couples):
        if self.follows:
            for p in [p for p in self.dancing_round.final_placings if p.couple.follow.number in couples]:
                self.skating.loc[p.couple.follow.number, p.dance.tag + "-" + p.adjudicator.tag] = p.final_placing
                self.skating.loc[p.couple.follow.number, RESULT] = 0
        else:
            for p in [p for p in self.dancing_round.final_placings if p.couple.number in couples]:
                self.skating.loc[p.couple.number, p.dance.tag + "-" + p.adjudicator.tag] = p.final_placing
                self.skating.loc[p.couple.number, RESULT] = 0
        for col in [c for c in self.placing_columns if c >= place]:
            for couple in couples:
                count = 0
                for adj in self.adjudicator_columns:
                    if self.skating.loc[couple, adj] <= col:
                        count += 1
                if self.skating.loc[couple, RESULT] == 0:
                    self.skating.loc[couple, col] = count
                else:
                    self.skating.loc[couple, col] = 0


class SkatingSummary:
    def __init__(self, dancing_round, follows=False, limited=False):
        self.follows = follows
        self.round = dancing_round
        if follows:
            self.couples = {c.number: c.follow.number for c in
                            sorted([c for c in dancing_round.couples], key=lambda x: x.follow.number)}
            self.reference_couples = {c.follow.number: c for c in
                                      sorted([c for c in dancing_round.couples], key=lambda x: x.follow.number)}
        else:
            self.couples = {num: num for num in sorted([c.number for c in dancing_round.couples])}
            self.reference_couples = {c.number: c for c in dancing_round.couples}
        self.dances = [d for d in dancing_round.dances]
        self.dances_columns = [d.tag for d in self.dances]
        columns = self.dances_columns + [TOTAL] + [RESULT]
        self.summary = pandas.DataFrame(index=self.couples.values(), columns=columns, dtype=object)
        self.summary[TOTAL] = [0 for _ in self.couples]
        self.summary[RESULT] = [0 for _ in self.couples]
        self.skating_dances = {d: SkatingDance(dancing_round, d, follows=follows) for d in self.dances}
        for d in self.dances:
            self.summary[d.tag] = self.skating_dances[d].skating[RESULT]
            for c in self.couples.values():
                self.summary.loc[c, TOTAL] += self.summary.loc[c, d.tag]
        if not limited:
            self.placing_columns = list(range(1, len(self.couples) + 1))
            self.summary_rule_10 = Rule10(dancing_round, follows=follows)
            self.summary_rule_11 = Rule11(dancing_round, follows=follows)
            for _ in self.couples:
                self.rule_9()
            for couple in [c for c in self.couples.values() if not self.summary_rule_10.skating.loc[c, RESULT] == ""]:
                self.summary_rule_10.skating.loc[couple, RESULT] = self.summary.loc[couple, RESULT]
            for couple in self.couples.values():
                if self.summary_rule_10.skating.loc[couple, RESULT] == 0:
                    self.summary_rule_10.skating.loc[couple, RESULT] = ""
            self.summary_rule_11.skating.fillna("", inplace=True)
            for couple in self.couples.values():
                if self.summary_rule_11.skating.loc[couple, RESULT] != "":
                    self.summary_rule_10.skating.loc[couple, RESULT] = ""
            for col in self.placing_columns:
                for couple in self.couples.values():
                    if self.summary_rule_11.skating.loc[couple, col] == 0:
                        self.summary_rule_11.skating.loc[couple, col] = "-"
            self.summary_rule_11.skating.drop(self.summary_rule_11.adjudicator_columns, inplace=True, axis=1)
            self.show_rule_10 = len([v for v in self.summary_rule_10.skating[RESULT].values if v != ""]) > 0
            self.show_rule_11 = len([v for v in self.summary_rule_11.skating[RESULT].values if v != ""]) > 0
            self.show_rules = self.show_rule_10 or self.show_rule_11

    def rule_9(self, couples=None):
        if couples is None:
            couples = self.couples.values()
        rule_9_couples = {c: self.summary.loc[c, TOTAL] for c in
                          [c for c in couples if self.summary.loc[c, RESULT] == 0]}
        if len(rule_9_couples) > 0:
            min_total = min(rule_9_couples.values())
            placings = [n for n in list(range(1, len(self.couples) + 1)) if n not in self.summary[RESULT].values]
            if list(rule_9_couples.values()).count(min_total) == 1:
                for c, p in rule_9_couples.items():
                    if rule_9_couples[c] == min_total:
                        self.summary.loc[c, RESULT] = min(placings)
                        break
            else:
                self.rule_10([c for c in rule_9_couples if rule_9_couples[c] == min_total])

    def rule_10(self, couples):
        places = [n for n in list(range(1, len(self.couples) + 1))
                  if n not in self.summary[RESULT].values][:len(couples)]
        place = places[0]
        rule_10_couples = {c: len([self.summary.loc[c, d] for d in self.dances_columns
                                   if self.summary.loc[c, d] <= place]) for c in
                           [c for c in couples if self.summary.loc[c, RESULT] == 0]}
        if len(rule_10_couples) > 0:
            max_places = max(rule_10_couples.values())
            min_places = min(rule_10_couples.values())
            for c in rule_10_couples:
                if rule_10_couples[c] > 0:
                    self.summary_rule_10.skating.loc[c, place] = rule_10_couples[c]
                    self.summary_rule_10.skating.loc[c, RESULT] = 0
            if list(rule_10_couples.values()).count(max_places) == 1:
                couple = [c for c in rule_10_couples if rule_10_couples[c] == max_places]
                self.summary.loc[couple[0], RESULT] = place
                del rule_10_couples[couple[0]]
                if len([c for c in rule_10_couples if rule_10_couples[c] != max_places]) > 1:
                    self.rule_10([c for c in rule_10_couples if rule_10_couples[c] != max_places])
            elif list(rule_10_couples.values()).count(min_places) == 1:
                couple = [c for c in rule_10_couples if rule_10_couples[c] == min_places]
                self.summary.loc[couple[0], RESULT] = places[-1]
                del rule_10_couples[couple[0]]
                if len([c for c in rule_10_couples if rule_10_couples[c] != min_places]) > 1:
                    self.rule_10([c for c in rule_10_couples if rule_10_couples[c] != min_places])
            else:
                rule_10_couples = {c: sum([self.summary.loc[c, d] for d in self.dances_columns
                                           if self.summary.loc[c, d] <= place]) for c in
                                   [c for c in couples if self.summary.loc[c, RESULT] == 0]
                                   if rule_10_couples[c] == max_places}
                if len(rule_10_couples) > 0:
                    min_sum_places = min(rule_10_couples.values())
                    max_sum_places = max(rule_10_couples.values())
                    for c in rule_10_couples:
                        if place > 1:
                            self.summary_rule_10.skating.loc[c, place] = \
                                str(self.summary_rule_10.skating.loc[c, place]) + \
                                "(" + str(int(rule_10_couples[c])) + ")"
                    if list(rule_10_couples.values()).count(min_sum_places) == 1:
                        couple = [c for c in rule_10_couples if rule_10_couples[c] == min_sum_places]
                        self.summary.loc[couple[0], RESULT] = place
                    elif list(rule_10_couples.values()).count(max_sum_places) == 1:
                        couple = [c for c in rule_10_couples if rule_10_couples[c] == max_sum_places]
                        self.summary.loc[couple[0], RESULT] = place
                    else:
                        self.rule_11([c for c in rule_10_couples if rule_10_couples[c] == min_sum_places], place)

    def rule_11(self, couples, place):
        if self.follows:
            rule_11_couples = {c: len([p for p in self.round.final_placings
                                       if p.final_placing <= place and p.couple.follow.number == c]) for c in couples}
        else:
            rule_11_couples = {c: len([p for p in self.round.final_placings
                                       if p.final_placing <= place and p.couple.number == c]) for c in couples}
        max_best_placings = max(rule_11_couples.values())
        for c in rule_11_couples:
            self.summary_rule_11.skating.loc[c, place] = rule_11_couples[c]
        if list(rule_11_couples.values()).count(max_best_placings) == 1:
            couple = [c for c in rule_11_couples if rule_11_couples[c] == max_best_placings]
            self.summary.loc[couple[0], RESULT] = place
            self.summary_rule_11.populate(place, couple)
            self.summary_rule_11.rule_5(place, couple, list(range(place, place + 1)))
            if len([c for c in rule_11_couples if rule_11_couples[c] != max_best_placings]) == 1:
                couple = [c for c in rule_11_couples if rule_11_couples[c] != max_best_placings]
                c = couple[0]
                self.summary.loc[couple[0], RESULT] = place + 1
                self.summary_rule_11.populate(place, couple)
                self.summary_rule_11.rule_5(place, couple, [place])
                self.summary_rule_11.skating.loc[c, RESULT] = place + 1
            if len([c for c in rule_11_couples if rule_11_couples[c] != max_best_placings]) > 1:
                self.rule_10([c for c in rule_11_couples if rule_11_couples[c] != max_best_placings])
        else:
            self.summary_rule_11.populate(place, [c for c in rule_11_couples])
            self.summary_rule_11.rule_5(place, [c for c in rule_11_couples],
                                        list(range(place, place + 1 + len(rule_11_couples))))
            for c in rule_11_couples:
                self.summary.loc[c, RESULT] = self.summary_rule_11.skating.loc[c, RESULT]

    def final_result_row(self):
        return sorted([{"couple": self.reference_couples[c], "placing": self.summary.loc[c, RESULT]}
                       for c in self.couples.values()], key=lambda x: x["placing"])

    def empty(self):
        for col in self.summary.columns:
            self.summary[col] = self.summary[col].astype(str)
            self.summary[col].values[:] = ""
        for col in self.summary_rule_10.skating.columns:
            self.summary_rule_10.skating[col] = self.summary_rule_10.skating[col].astype(str)
            self.summary_rule_10.skating[col].values[:] = ""
        for col in self.summary_rule_11.skating.columns:
            self.summary_rule_11.skating[col] = self.summary_rule_11.skating[col].astype(str)
            self.summary_rule_11.skating[col].values[:] = ""
        for d in self.skating_dances:
            for col in self.skating_dances[d].skating.columns:
                self.skating_dances[d].skating[col] = self.skating_dances[d].skating[col].astype(str)
                self.skating_dances[d].skating[col].values[:] = ""
        return self


class CompetitionResult:
    def __init__(self, competition, follows=False):
        super().__init__()
        if competition.is_random_single_partner() or competition.is_change_per_round():
            self.couples = [c.number for c in competition.rounds[0].couples]
        elif competition.is_change_per_dance():
            if follows:
                self.couples = [f.number for f in competition.follows]
            else:
                self.couples = [l.number for l in competition.leads]
        else:
            self.couples = [c.number for c in competition.couples]
        self.couples = sorted(self.couples)
        self.adjudicators = competition.adjudicators
        self.index = []
        for dancing_round in competition.rounds:
            if not dancing_round.is_general_look():
                previous_round = dancing_round.previous_round()
                if previous_round is not None:
                    if not previous_round.is_general_look():
                        self.index += [str(dancing_round.round_id) + QUALIFIED]
                if not dancing_round.is_final():
                    self.index += [str(dancing_round.round_id) + str(adj.tag)
                                   for adj in competition.adjudicators] + [str(dancing_round.round_id) + RESULT]
                else:
                    self.index += [str(dancing_round.round_id) + RESULT]
        self.table = pandas.DataFrame(index=self.index, columns=[FIRST] + self.couples)
        self.table = self.table.fillna(0)
        for dancing_round in competition.rounds:
            if not dancing_round.is_general_look():
                self.table.loc[str(dancing_round.round_id) + RESULT, FIRST] = f"Result of {dancing_round.type.value}"
                previous_round = dancing_round.previous_round()
                if previous_round is not None:
                    if not previous_round.is_general_look():
                        self.table.loc[str(dancing_round.round_id) + QUALIFIED, FIRST] = \
                            f"Qualified for {dancing_round.type.value}"
                if not dancing_round.is_final():
                    for adj in self.adjudicators:
                        self.table.loc[str(dancing_round.round_id) + str(adj.tag), FIRST] = adj.name
                    for mark in dancing_round.marks():
                        if mark.mark:
                            if follows:
                                self.table.loc[str(dancing_round.round_id) +
                                               str(mark.adjudicator.tag), mark.couple.follow.number] += 1
                                self.table.loc[str(dancing_round.round_id) + RESULT, mark.couple.follow.number] += 1
                            else:
                                self.table.loc[str(dancing_round.round_id) +
                                               str(mark.adjudicator.tag), mark.couple.number] += 1
                                self.table.loc[str(dancing_round.round_id) + RESULT, mark.couple.number] += 1
                    if not (dancing_round.is_first_round() and dancing_round.is_general_look()):
                        for couple in self.couples:
                            if follows:
                                couples = {c.number: c.follow.number for c in dancing_round.couples}
                            else:
                                couples = {c.number: c.number for c in dancing_round.couples}
                            if couple in couples.values():
                                if previous_round is not None:
                                    if not previous_round.is_general_look():
                                        self.table.loc[str(dancing_round.round_id) + QUALIFIED, couple] = "x"
                            else:
                                if previous_round is not None:
                                    if not previous_round.is_general_look():
                                        self.table.loc[str(dancing_round.round_id) + QUALIFIED, couple] = ""
                                self.table.loc[str(dancing_round.round_id) + RESULT, couple] = ""
                                for adj in self.adjudicators:
                                    self.table.loc[str(dancing_round.round_id) + str(adj.tag), couple] = ""
                else:
                    skating = dancing_round.skating_summary(follows=follows)
                    if follows:
                        couples = {c.number: c.follow.number for c in dancing_round.couples}
                    else:
                        couples = {c.number: c.number for c in dancing_round.couples}
                    for couple in self.couples:
                        if couple in couples.values():
                            if previous_round is not None:
                                if not previous_round.is_general_look():
                                    self.table.loc[str(dancing_round.round_id) + QUALIFIED, couple] = "x"
                            self.table.loc[str(dancing_round.round_id) + RESULT, couple] = \
                                skating.summary.loc[couple, RESULT]
                        else:
                            if previous_round is not None:
                                if not previous_round.is_general_look():
                                    self.table.loc[str(dancing_round.round_id) + QUALIFIED, couple] = ""
                            self.table.loc[str(dancing_round.round_id) + RESULT, couple] = ""
            self.index_column = self.table[FIRST]
        for c in self.couples:
            for i in self.index:
                with suppress(ValueError):
                    self.table.loc[i, c] = int(self.table.loc[i, c])


def generate_placings(results, counter=1):
    unique_results = list(set([r for r in results if r != -1]))
    unique_results.sort(reverse=True)
    result_placing = {}
    for i in set(results):
        result_placing.update({i: results.count(i)})
    result_map = {}
    for i in unique_results:
        if result_placing[i] == 1:
            result_map.update({i: str(counter)})
        else:
            result_map.update({i: str(counter) + "-" + str(counter + result_placing[i] - 1)})
        counter += result_placing[i]
    return result_map


class RankingReport:
    def __init__(self, competition, follows=False):
        super().__init__()
        self.competition = competition
        self.rounds = sorted([r for r in self.competition.rounds if r.is_completed()],
                             key=lambda x: x.round_id, reverse=True)
        if follows:
            self.reference_couples = {c.follow.number: c for c in competition.rounds[0].couples}
        else:
            self.reference_couples = {c.number: c for c in competition.rounds[0].couples}
        if competition.is_change_per_dance():
            self.adjudicators = competition.adjudicators_for_role(FOLLOW if follows else LEAD)
        else:
            self.adjudicators = competition.sorted_adjudicators()
        self.placings = {}
        self.skating_results = {}
        self.added_couples = []
        for r in self.rounds:
            if r.is_final():
                if r not in self.skating_results:
                    self.skating_results[r] = r.skating_summary(follows=follows)
        if follows:
            for r in self.rounds:
                if r.is_final():
                    for res in self.skating_results[r].final_result_row():
                        if res["couple"].follow.number not in self.added_couples:
                            self.placings[len(self.placings)+1] = {"couple": res["couple"].follow.number,
                                                                   "placing": res["placing"],
                                                                   "number": res["couple"].follow.number}
                            self.added_couples.append(res["couple"].follow.number)
                else:
                    if not r.competition.is_change_per_dance():
                        placings_map = generate_placings([res.marks for res in r.round_results
                                                          if res.couple.follow.number
                                                          not in self.added_couples], counter=len(self.placings)+1)
                        for res in sorted([res for res in r.round_results], key=lambda x: x.marks, reverse=True):
                            if res.couple.follow.number not in self.added_couples:
                                self.placings[len(self.placings) + 1] = {"couple": res.couple.follow.number,
                                                                         "placing": placings_map[res.marks],
                                                                         "number": res.couple.follow.number}
                                self.added_couples.append(res.couple.follow.number)
                    else:
                        dancers_list = [res for res in r.round_results if res.follow
                                        and res.couple.follow.number not in self.added_couples]
                        placings_map = generate_placings([d.marks for d in dancers_list],
                                                         counter=len(self.placings) + 1)
                        for res in sorted([res for res in dancers_list], key=lambda x: x.marks, reverse=True):
                            self.placings[len(self.placings) + 1] = \
                                {"couple": res.couple.follow.number, "placing": placings_map[res.marks],
                                 "number": res.couple.follow.number}
                            self.added_couples.append(res.couple.follow.number)
            self.results = {rc: {r: {d: {a.adjudicator: None for a in self.adjudicators} for d in r.sorted_dances()}
                                 for r in self.rounds if rc in [c.follow.number for c in r.couples]}
                            for rc in self.reference_couples}
            for couple in self.results:
                for r in self.rounds:
                    if couple in [c.follow.number for c in r.couples]:
                        for dance in r.sorted_dances():
                            if r.is_final():
                                for a in self.adjudicators:
                                    self.results[couple][r][dance][a.adjudicator] = \
                                        self.skating_results[r].skating_dances[dance].skating[a.adjudicator.tag][couple]
                                self.results[couple][r][dance][SUM] = \
                                    self.skating_results[r].summary[dance.tag][couple]
                            else:
                                marks = [m for m in r.ordered_marks(dance_id=dance.dance_id)
                                         if m.adjudicator in [a.adjudicator for a in self.adjudicators]]
                                for mark in marks:
                                    self.results[mark.couple.follow.number][r][dance][mark.adjudicator] = \
                                        "x" if mark.mark else "-"
                                self.results[couple][r][dance][SUM] = \
                                    len([m for m in marks if m.couple.follow.number == couple and m.mark])
                        if r.is_final():
                            self.results[couple][r][TOTAL] = self.skating_results[r].summary[TOTAL][couple]
                        else:
                            marks = [m for m in r.ordered_marks() if m.adjudicator
                                     in [a.adjudicator for a in self.adjudicators]]
                            self.results[couple][r][TOTAL] = \
                                len([m for m in marks if m.couple.follow.number == couple and m.mark])
        else:
            for r in self.rounds:
                if r.is_final():
                    for res in self.skating_results[r].final_result_row():
                        if res["couple"].number not in self.added_couples:
                            self.placings[len(self.placings)+1] = \
                                {"couple": res["couple"].number, "placing": res["placing"],
                                 "number": res["couple"].number}
                            self.added_couples.append(res["couple"].number)
                else:
                    if not r.competition.is_change_per_dance():
                        placings_map = generate_placings([res.marks for res in r.round_results if res.couple.number
                                                          not in self.added_couples], counter=len(self.placings)+1)
                        for res in sorted([res for res in r.round_results], key=lambda x: x.marks, reverse=True):
                            if res.couple.number not in self.added_couples:
                                self.placings[len(self.placings) + 1] = \
                                    {"couple": res.couple.number, "placing": placings_map[res.marks],
                                     "number": res.couple.number}
                                self.added_couples.append(res.couple.number)
                    else:
                        dancers_list = [res for res in r.round_results if not res.follow
                                        and res.couple.number not in self.added_couples]
                        placings_map = generate_placings([d.marks for d in dancers_list],
                                                         counter=len(self.placings) + 1)
                        for res in sorted([res for res in dancers_list], key=lambda x: x.marks, reverse=True):
                            self.placings[len(self.placings) + 1] = \
                                {"couple": res.couple.number, "placing": placings_map[res.marks],
                                 "number": res.couple.number}
                            self.added_couples.append(res.couple.number)
            self.results = {rc: {r: {d: {a.adjudicator: None for a in self.adjudicators} for d in r.sorted_dances()}
                                 for r in self.rounds if rc in [c.number for c in r.couples]}
                            for rc in self.reference_couples}
            for couple in self.results:
                for r in self.rounds:
                    if couple in [c.number for c in r.couples]:
                        for dance in r.sorted_dances():
                            if r.is_final():
                                for a in self.adjudicators:
                                    self.results[couple][r][dance][a.adjudicator] = \
                                        self.skating_results[r].skating_dances[dance].skating[a.adjudicator.tag][couple]
                                self.results[couple][r][dance][SUM] = \
                                    self.skating_results[r].summary[dance.tag][couple]
                            else:
                                marks = [m for m in r.ordered_marks(dance_id=dance.dance_id)
                                         if m.adjudicator in [a.adjudicator for a in self.adjudicators]]
                                for mark in marks:
                                    self.results[mark.couple.number][r][dance][mark.adjudicator] = \
                                        "x" if mark.mark else "-"
                                self.results[couple][r][dance][SUM] = \
                                    len([m for m in marks if m.couple.number == couple and m.mark])
                        if r.is_final():
                            self.results[couple][r][TOTAL] = self.skating_results[r].summary[TOTAL][couple]
                        else:
                            marks = [m for m in r.ordered_marks() if m.adjudicator
                                     in [a.adjudicator for a in self.adjudicators]]
                            self.results[couple][r][TOTAL] = \
                                len([m for m in marks if m.couple.number == couple and m.mark])
        self.round_count = {r: i for i, r in enumerate(sorted([r for r in self.rounds if not r.is_final()
                                                               and not r.is_semi_final() and not r.is_re_dance()],
                                                              key=lambda x: x.round_id), 1)}
        self.round_count.update({r: r.short_name() for r in self.rounds if r.is_final()
                                 or r.is_semi_final() or r.is_re_dance()})

    def json(self, role=None):
        follows = role == FOLLOW
        leads = role == LEAD
        rank = {
            place: {
                "number": self.reference_couples[v["number"]].follow.number
                if follows else self.reference_couples[v["number"]].number,
                "rank": str(v["placing"]),
                "name": self.reference_couples[v["number"]].follow.name
                if follows else self.reference_couples[v["number"]].lead.name
                if leads else self.reference_couples[v["number"]].names(),
                "team": self.reference_couples[v["number"]].follow.team
                if follows else self.reference_couples[v["number"]].team(),
            } for place, v in self.placings.items()
        }
        rounds = {
            r.round_id: {
                "round_id": r.round_id,
                "tag": self.round_count[r],
                "order": i,
            } for i, r in enumerate(self.rounds)
        }
        used_adjudicators = sorted(
            self.competition.adjudicators_for_role(role if role == LEAD or role == FOLLOW else None),
            key=lambda a: a.adjudicator.tag
        )
        results = {
            self.reference_couples[rc].follow.number if follows else self.reference_couples[rc].number: {
                r.round_id: {**{
                    d.dance_id: {**{
                        a.adjudicator.adjudicator_id: self.results[rc][r][d][a.adjudicator] for a in used_adjudicators
                    }, **{"sum": str(self.results[rc][r][d][SUM])}} for d in r.sorted_dances()
                }, **{"total": str(self.results[rc][r][TOTAL])}} for r in self.rounds
                if rc in [c.follow.number if follows else c.number for c in r.couples]
            } for rc in self.reference_couples
        }
        adjudicators = [a.json() for a in used_adjudicators]
        dances = [d.json() for d in self.competition.last_round().sorted_dances()]
        return {
            "rank": rank,
            "rounds": rounds,
            "results": results,
            "adjudicators": adjudicators,
            "dances": dances,
        }
