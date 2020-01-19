import enum


class CompetitionMode(enum.Enum):
    single_partner = "Single partner"
    random_single_partner = "Random single partner"
    change_per_round = "Change partner per round"
    change_per_dance = "Change partner per dance"


COMPETITION_SHORT_NAMES = {CompetitionMode.single_partner: "SP", CompetitionMode.random_single_partner: "RSP",
                           CompetitionMode.change_per_round: "CPR", CompetitionMode.change_per_dance: "CPD"}

CHANGE_MODES = [CompetitionMode.change_per_dance, CompetitionMode.change_per_round]
