import enum


class RoundType(enum.Enum):
    qualification = "Qualification"
    general_look = "General look"
    first_round = "First round"
    re_dance = "Re-dance"
    second_round = "Second round"
    intermediate_round = "Intermediate round"
    eight_final = "Eight final"
    quarter_final = "Quarter final"
    semi_final = "Semi-final"
    final = "Final"


ROUND_SHORT_NAMES = {
    RoundType.qualification: "Q",
    RoundType.general_look: "GL", RoundType.first_round: "1st", RoundType.second_round: "2nd",
    RoundType.re_dance: "Re", RoundType.intermediate_round: "IR", RoundType.eight_final: "EF", 
    RoundType.quarter_final: "QF", RoundType.semi_final: "SF", RoundType.final: "F"
}
