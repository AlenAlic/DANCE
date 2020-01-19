import enum
from backend.constants import LEAD, FOLLOW


class AdjudicatorAssignmentEnum(enum.Enum):
    lead = LEAD
    follow = FOLLOW
    both = "Couple"
