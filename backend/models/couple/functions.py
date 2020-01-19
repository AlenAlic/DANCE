from backend.models import db
from backend.models.couple import Couple
from backend.util import shift_list


def generate_new_couples_from_dancers(leads, follows):
    created_couples = []
    for idx, lead in enumerate(leads):
        couple = Couple.query.filter(Couple.lead == leads[idx], Couple.follow == follows[idx]).first()
        if couple is None:
            couple = Couple()
            couple.number = leads[idx].number
            couple.lead = leads[idx]
            couple.follow = follows[idx]
            db.session.add(couple)
        created_couples.append(couple)
    return created_couples


def generate_new_couples_from_couples(couples, offset=0):
    leads = [c.lead for c in couples]
    follows = [c.follow for c in couples]
    return generate_new_couples_from_dancers(leads, shift_list(follows, offset=offset))
