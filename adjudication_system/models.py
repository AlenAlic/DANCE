from adjudication_system import db, login
from flask import current_app, url_for, redirect, flash
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import datetime
import random
from random import shuffle
from adjudication_system.values import *
import itertools
from adjudication_system.skating import SkatingDance, SkatingSummary, CompetitionResult, RankingReport
from functools import wraps


TABLE_EVENT = 'event'
TABLE_COMPETITION = 'competition'
TABLE_DANCING_CLASS = 'dancing_class'
TABLE_DISCIPLINE = 'discipline'
TABLE_DANCE = 'dance'
TABLE_ADJUDICATOR = 'adjudicator'
TABLE_DANCER = 'dancer'
TABLE_COUPLE = 'couple'
TABLE_ROUND = 'round'
TABLE_DANCE_ACTIVE = 'dance_active'
TABLE_HEAT = 'heat'
TABLE_MARK = 'mark'
TABLE_FINAL_PLACING = 'final_placing'
TABLE_COUPLE_PRESENT = 'couple_present'
TABLE_ROUND_RESULT = 'round_result'

TABLE_COMPETITION_LEAD = 'competition_lead'
TABLE_COMPETITION_FOLLOW = 'competition_follow'
TABLE_COMPETITION_COUPLE = 'competition_couple'
TABLE_COMPETITION_ADJUDICATOR = 'competition_adjudicator'
TABLE_ROUND_DANCE = 'round_dance'
TABLE_ROUND_COUPLE = 'round_couple'
TABLE_HEAT_COUPLE = 'heat_couple'


ADJUDICATOR_SYSTEM_TABLES = [
    TABLE_EVENT,
    TABLE_COMPETITION,
    TABLE_DANCING_CLASS,
    TABLE_DISCIPLINE,
    TABLE_DANCE,
    TABLE_ADJUDICATOR,
    TABLE_DANCER,
    TABLE_COUPLE,
    TABLE_ROUND,
    TABLE_DANCE_ACTIVE,
    TABLE_HEAT,
    TABLE_MARK,
    TABLE_FINAL_PLACING,
    TABLE_COUPLE_PRESENT,
    TABLE_ROUND_RESULT,
    TABLE_COMPETITION_LEAD,
    TABLE_COMPETITION_FOLLOW,
    TABLE_COMPETITION_COUPLE,
    TABLE_COMPETITION_ADJUDICATOR,
    TABLE_ROUND_DANCE,
    TABLE_ROUND_COUPLE,
    TABLE_HEAT_COUPLE,
]


def requires_access_level(access_levels):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.access not in access_levels:
                flash("Page inaccessible.")
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def requires_adjudicator_access_level(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_adjudicator():
            flash("Page inaccessible.")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer, index=True, nullable=False)
    adjudicator_id = db.Column(db.Integer, db.ForeignKey('adjudicator.adjudicator_id'))
    adjudicator = db.relationship('Adjudicator', backref=db.backref("user", uselist=False), single_parent=True,
                                  cascade='all, delete-orphan')

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '{}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_tournament_office_manager(self):
        return self.access == ACCESS[TOURNAMENT_OFFICE_MANAGER]

    def is_floor_manager(self):
        return self.access == ACCESS[FLOOR_MANAGER]

    def is_adjudicator(self):
        return self.access == ACCESS[ADJUDICATOR]

    def is_presenter(self):
        return self.access == ACCESS[PRESENTER]


class Event(db.Model):
    __tablename__ = TABLE_EVENT
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    competitions = db.relationship('Competition', back_populates='event', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '{}'.format(self.name)

    def has_competitions(self):
        return len(self.competitions) > 0

    def unique_dates(self):
        return list(sorted(set([c.when.date() for c in self.competitions])))

    def competitions_by_date(self):
        return list(sorted([c for c in self.competitions], key=lambda x: x.when))

    def competitions_on_day(self, date):
        return list(sorted([c for c in self.competitions if c.when.date() == date], key=lambda x: x.when))


competition_lead_table = db.Table(
    TABLE_COMPETITION_LEAD, db.Model.metadata,
    db.Column('competition_id', db.Integer,
              db.ForeignKey('competition.competition_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('dancer_id', db.Integer, db.ForeignKey('dancer.dancer_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('competition_id', 'dancer_id', name='_competition_lead_uc')
)


competition_follow_table = db.Table(
    TABLE_COMPETITION_FOLLOW, db.Model.metadata,
    db.Column('competition_id', db.Integer,
              db.ForeignKey('competition.competition_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('dancer_id', db.Integer, db.ForeignKey('dancer.dancer_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('competition_id', 'dancer_id', name='_competition_follow_uc')
)


competition_couple_table = db.Table(
    TABLE_COMPETITION_COUPLE, db.Model.metadata,
    db.Column('competition_id', db.Integer,
              db.ForeignKey('competition.competition_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('couple_id', db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('competition_id', 'couple_id', name='_competition_couple_uc')
)


competition_adjudicator_table = db.Table(
    TABLE_COMPETITION_ADJUDICATOR, db.Model.metadata,
    db.Column('competition_id', db.Integer,
              db.ForeignKey('competition.competition_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('adjudicator_id', db.Integer,
              db.ForeignKey('adjudicator.adjudicator_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('competition_id', 'adjudicator_id', name='_competition_adjudicator_uc')
)


class CompetitionMode(enum.Enum):
    single_partner = "Single partner"
    random_single_partner = "Random single partner"
    change_per_round = "Change partner per round"
    change_per_dance = "Change partner per dance"


COMPETITION_SHORT_NAMES = {CompetitionMode.single_partner: 'SP', CompetitionMode.random_single_partner: 'RSP',
                           CompetitionMode.change_per_round: 'CPR', CompetitionMode.change_per_dance: 'CPD'}
CHANGE_MODES = [CompetitionMode.change_per_dance, CompetitionMode.change_per_round]


class Competition(db.Model):
    __tablename__ = TABLE_COMPETITION
    competition_id = db.Column(db.Integer, primary_key=True)
    dancing_class_id = db.Column(db.Integer, db.ForeignKey('dancing_class.dancing_class_id',
                                                           onupdate="CASCADE", ondelete="CASCADE"))
    dancing_class = db.relationship("DancingClass", back_populates="competitions")
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.discipline_id',
                                                        onupdate="CASCADE", ondelete="CASCADE"))
    discipline = db.relationship("Discipline", back_populates="competitions")
    floors = db.Column(db.Integer, default=1)
    when = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    rounds = db.relationship("Round", back_populates="competition", cascade='all, delete, delete-orphan')
    mode = db.Column(db.Enum(CompetitionMode), default=CompetitionMode.single_partner)
    results_published = db.Column(db.Boolean, nullable=False, default=False)
    couples = db.relationship("Couple", secondary=competition_couple_table, back_populates="competitions")
    leads = db.relationship("Dancer", secondary=competition_lead_table, back_populates="competitions_lead")
    follows = db.relationship("Dancer", secondary=competition_follow_table, back_populates="competitions_follow")
    adjudicators = db.relationship("Adjudicator", secondary=competition_adjudicator_table)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id', onupdate="CASCADE", ondelete="CASCADE"))
    event = db.relationship("Event", back_populates="competitions", single_parent=True)
    qualification_id = db.Column(db.Integer, db.ForeignKey('competition.competition_id',
                                                           onupdate="CASCADE", ondelete="CASCADE"))
    qualifications = db.relationship("Competition", backref=db.backref('qualification', remote_side=[competition_id]))

    def __repr__(self):
        return '{disc} {cls}'.format(cls=self.dancing_class, disc=self.discipline)

    def name(self):
        return self.__repr__()

    def short_repr(self):
        return f'{self.discipline.name[:2]}{self.dancing_class.name[:2]}'

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

    def has_adjudicators(self):
        return len(self.adjudicators) > 0

    def result(self, follows=False):
        return CompetitionResult(self, follows=follows)

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

    def can_create_first_round(self):
        return len(self.adjudicators) > 0 and self.has_contestants() and not self.has_rounds() \
               and self.equal_leads_follows()

    def max_couples(self):
        return max(len(self.couples), len(self.leads), len(self.follows))

    def generate_couples(self):
        if self.mode == CompetitionMode.single_partner:
            return self.couples
        elif self.mode == CompetitionMode.random_single_partner:
            return create_couples_list(leads=self.leads, follows=self.follows)
        elif self.mode == CompetitionMode.change_per_round or self.mode == CompetitionMode.change_per_dance:
            return create_couples_list(leads=self.leads, follows=self.follows)

    def is_single_partner(self):
        return self.mode == CompetitionMode.single_partner

    def is_random_single_partner(self):
        return self.mode == CompetitionMode.random_single_partner

    def is_change_per_round(self):
        return self.mode == CompetitionMode.change_per_round

    def is_change_per_dance(self):
        return self.mode == CompetitionMode.change_per_dance

    def short_mode_name(self):
        return COMPETITION_SHORT_NAMES[self.mode]

    def has_rounds(self):
        return len(self.rounds) > 0

    def change_per_round_partner_list(self):
        rounds = [r for r in self.rounds]
        leads = {l: {r: '-' for r in self.rounds} for l in sorted([l.number for l in self.leads])}
        follows = {f: {r: '-' for r in self.rounds} for f in sorted([f.number for f in self.follows])}
        for r in self.rounds:
            for couple in r.couples:
                leads[couple.lead.number][r] = couple.follow.number
                follows[couple.follow.number][r] = couple.lead.number
        return leads, follows, rounds

    def is_configurable(self):
        if self.first_round() is None:
            return True
        else:
            return not self.first_round().has_heats()

    def competitors(self, numbers_only=False):
        if not numbers_only:
            if self.mode == CompetitionMode.single_partner:
                return f"{len(self.couples)} couple{'' if len(self.couples) == 1 else 's'}"
            else:
                return f"{len(self.leads)} lead{'' if len(self.leads) == 1 else 's'} / {len(self.follows)} " \
                    f"follow{'' if len(self.follows) == 1 else 's'}"
        else:
            if self.mode == CompetitionMode.single_partner:
                return f"{len(self.couples)}"
            else:
                return f"{len(self.leads)}/{len(self.follows)}"

    def dancers(self):
        return [d for d in self.leads + self.follows]

    def presenter_rounds(self):
        return [{"id": r.round_id,
                 "type": r.type.name,
                 "name": r.type.value,
                 "completed": r.is_completed(),
                 "mode": r.competition.mode.name
                 } for r in self.rounds]

    def last_round_with_heat_list_published(self):
        rounds = [r for r in self.rounds if r.heat_list_published and r.type != RoundType.final]
        if len(rounds) > 0:
            return max(rounds, key=lambda x: x.round_id)
        return None

    def has_completed_final(self):
        rounds = [r for r in self.rounds if r.type == RoundType.final]
        if len(rounds) > 0:
            for r in rounds:
                return r.final_completed()
        return False

    def is_quali_competition(self):
        rounds = [r for r in self.rounds if r.type == RoundType.qualification]
        if len(rounds) == 1:
            return True
        return False

    def cache(self):
        return RESULTS_CACHE.format(self.competition_id)


def create_couples_list(couples=None, leads=None, follows=None):
    if couples is not None:
        leads = [c.lead for c in couples]
        follows = [c.follow for c in couples]
    else:
        leads = [d for d in leads]
        follows = [d for d in follows]
    random.shuffle(leads)
    random.shuffle(follows)
    dancers = zip(leads, follows)
    couples = []
    for d in dancers:
        couple = Couple.query.filter(Couple.lead == d[0], Couple.follow == d[1]).first()
        if couple is None:
            couple = Couple()
            couple.number = d[0].number
            couple.lead = d[0]
            couple.follow = d[1]
            db.session.add(couple)
        couples.append(couple)
    db.session.commit()
    return couples


class DancingClass(db.Model):
    __tablename__ = TABLE_DANCING_CLASS
    dancing_class_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    competitions = db.relationship("Competition", back_populates="dancing_class")

    def __repr__(self):
        return '{}'.format(self.name)

    def has_competitions(self):
        return len(self.competitions) > 0

    def deletable(self):
        return not self.has_competitions()


class Discipline(db.Model):
    __tablename__ = TABLE_DISCIPLINE
    discipline_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    competitions = db.relationship("Competition", back_populates="discipline")
    dances = db.relationship("Dance", back_populates="discipline")

    def __repr__(self):
        return '{}'.format(self.name)

    def has_competitions(self):
        return len(self.competitions) > 0

    def has_dances(self):
        return len(self.dances) > 0

    def deletable(self):
        return not self.has_competitions() and not self.has_dances()


round_dance_table = db.Table(
    TABLE_ROUND_DANCE, db.Model.metadata,
    db.Column('round_id', db.Integer, db.ForeignKey('round.round_id',  onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('dance_id', db.Integer, db.ForeignKey('dance.dance_id',  onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('round_id', 'dance_id', name='_round_dance_uc')
)

round_couple_table = db.Table(
    TABLE_ROUND_COUPLE, db.Model.metadata,
    db.Column('round_id', db.Integer, db.ForeignKey('round.round_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('couple_id', db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('round_id', 'couple_id', name='_round_couple_uc')
)


heat_couple_table = db.Table(
    TABLE_HEAT_COUPLE, db.Model.metadata,
    db.Column('heat_id', db.Integer, db.ForeignKey('heat.heat_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.Column('couple_id', db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE")),
    db.UniqueConstraint('heat_id', 'couple_id', name='_heat_couple_uc')
)


class Dance(db.Model):
    __tablename__ = TABLE_DANCE
    dance_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    tag = db.Column(db.String(6), unique=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.discipline_id',
                                                        onupdate="CASCADE", ondelete="CASCADE"))
    discipline = db.relationship("Discipline", back_populates="dances")

    def __repr__(self):
        return '{}'.format(self.name)

    def has_discipline(self):
        return self.discipline is not None

    def deletable(self):
        return not self.has_discipline()


class Adjudicator(db.Model):
    __tablename__ = TABLE_ADJUDICATOR
    adjudicator_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    tag = db.Column(db.String(6), unique=True)
    dance = db.Column(db.Integer, nullable=False, default=0)
    round = db.Column(db.Integer, nullable=False, default=0)
    competitions = db.relationship("Competition", secondary=competition_adjudicator_table,
                                   back_populates="adjudicators")

    def __repr__(self):
        return '{}'.format(self.name)

    def has_assignments(self):
        return len(self.competitions) > 0

    def assignments(self):
        return len(self.competitions)

    def assignments_on_day(self, date):
        return len([c for c in self.competitions if c.when.date() == date])

    def deletable(self):
        return len(self.competitions) == 0

    def active_round(self):
        if self.round != 0:
            return f"{Round.query.filter(Round.round_id == self.round).first()}"
        return "Offline"

    def active_dance(self):
        if self.dance != 0:
            return f"{Dance.query.filter(Dance.dance_id == self.dance).first()}"
        return "Offline"

    def is_present(self, r):
        return r.round_id == self.round


class Dancer(db.Model):
    __tablename__ = TABLE_DANCER
    __table_args__ = (db.UniqueConstraint('number', 'role', name='_number_role_uc'),)
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
        return f'{self.name}'

    def partners(self):
        if self.role == LEAD:
            return [(c.follow, c.participating_competitions()) for c in self.couples_lead]
        else:
            return [(c.lead, c.participating_competitions()) for c in self.couples_follow]

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

    def append_competition(self, comp):
        if comp is not None:
            if comp.mode != CompetitionMode.single_partner:
                if self.role == LEAD:
                    if comp not in self.competitions_lead:
                        self.competitions_lead.append(comp)
                else:
                    if comp not in self.competitions_follow:
                        self.competitions_follow.append(comp)

    def set_competitions(self, comps):
        if self.role == LEAD:
            self.competitions_lead = [c for c in self.competitions_lead if c.has_rounds()] + comps
        else:
            self.competitions_follow = [c for c in self.competitions_follow if c.has_rounds()] + comps


class Couple(db.Model):
    __tablename__ = TABLE_COUPLE
    __table_args__ = (db.UniqueConstraint('lead_id', 'follow_id', name='_lead_follow_uc'),)
    couple_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    lead_id = db.Column(db.Integer, db.ForeignKey('dancer.dancer_id', onupdate="CASCADE", ondelete="CASCADE"))
    lead = db.relationship("Dancer", back_populates="couples_lead", foreign_keys="Couple.lead_id")
    follow_id = db.Column(db.Integer, db.ForeignKey('dancer.dancer_id', onupdate="CASCADE", ondelete="CASCADE"))
    follow = db.relationship("Dancer",  back_populates="couples_follow", foreign_keys="Couple.follow_id")
    competitions = db.relationship("Competition", secondary=competition_couple_table, back_populates="couples")
    rounds = db.relationship("Round", secondary=round_couple_table, back_populates="couples")
    heats = db.relationship("Heat", secondary=heat_couple_table)

    def __repr__(self):
        return '{number} - {lead} - {follow}'.format(number=self.number, lead=self.lead, follow=self.follow)

    def participating_competitions(self):
        if len(self.competitions) > 0:
            return [c for c in self.competitions if c.dancing_class.name != TEST]
        else:
            return list(set([r.competition for r in self.rounds + [h.round for h in self.heats]]))

    def deletable(self):
        return len(self.rounds) == 0 and len(self.heats) == 0

    def teams(self):
        if self.lead.team == self.follow.team:
            return self.lead.team
        else:
            return f"{self.lead.team} / {self.follow.team}"

    def names(self):
        return f"{self.lead.name} / {self.follow.name}"


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
    RoundType.general_look: 'GL', RoundType.first_round: '1st', RoundType.second_round: 'SR', RoundType.re_dance: 'R',
    RoundType.intermediate_round: 'I', RoundType.eight_final: 'EF', RoundType.quarter_final: 'QF',
    RoundType.semi_final: 'SF', RoundType.final: 'F'
}


class Round(db.Model):
    __tablename__ = TABLE_ROUND
    round_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(RoundType))
    min_marks = db.Column(db.Integer, default=1)
    max_marks = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=False)
    heat_list_published = db.Column(db.Boolean, default=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.competition_id',
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    competition = db.relationship("Competition", back_populates="rounds")
    dances = db.relationship("Dance", secondary=round_dance_table)
    couples = db.relationship("Couple", secondary=round_couple_table, back_populates="rounds")
    heats = db.relationship("Heat", back_populates="round", cascade='all, delete, delete-orphan')
    round_results = db.relationship("RoundResult", back_populates="round", cascade='all, delete, delete-orphan')
    dance_active = db.relationship("DanceActive", back_populates="round", cascade='all, delete, delete-orphan')
    final_placings = db.relationship("FinalPlacing", back_populates="round", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '{comp} {type}'.format(comp=self.competition, type=self.type.value)

    def short_name(self):
        return ROUND_SHORT_NAMES[self.type]

    def is_published(self):
        if self.competition.heat_list is None:
            return False
        return self.__repr__() in self.competition.heat_list

    def is_completed(self):
        if not self.is_final():
            return len(self.round_results) > 0
        else:
            return self.final_completed()

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

    def previous_round(self):
        previous_rounds = [r.round_id for r in self.competition.rounds if r.round_id < self.round_id]
        try:
            previous_rounds = [r for r in self.competition.rounds if r.round_id == max(previous_rounds)]
        except ValueError:
            return None
        else:
            return previous_rounds[0]

    def first_round_after_qualification_split(self):
        return self.type == RoundType.first_round and len(self.heats) == 0 \
               and self.competition.qualification is not None

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

    def is_semi_final(self):
        return self.type == RoundType.semi_final

    def is_final(self):
        return self.type == RoundType.final

    def round_completed(self):
        return len(self.round_results) > 0

    def is_split(self):
        return sum([len(c.rounds) for c in [q for q in self.competition.qualifications]]) > 0

    def has_adjudicators(self):
        return len(self.competition.adjudicators) > 0

    def first_dance(self):
        try:
            dances = [d for d in self.dances if d.name in DANCE_ORDER[self.competition.discipline.name]]
            dances.sort(key=lambda x: DANCE_ORDER[self.competition.discipline.name][x.name])
            return dances[0]
        except KeyError:
            return self.dances[0]
        except IndexError:
            return self.dances[0]

    def previous_dance(self, dance):
        try:
            dances = [d for d in self.dances if d.dance_id < dance.dance_id]
            dances.sort(key=lambda x: DANCE_ORDER[self.competition.discipline.name][x.name])
            return dances[-1]
        except KeyError:
            return None
        except IndexError:
            return None

    def next_dance(self, dance):
        try:
            dances = [d for d in self.dances if d.dance_id > dance.dance_id]
            dances.sort(key=lambda x: DANCE_ORDER[self.competition.discipline.name][x.name])
            return dances[0]
        except KeyError:
            return None
        except IndexError:
            return None

    def last_dance(self):
        try:
            dances = [d for d in self.dances]
            dances.sort(key=lambda x: DANCE_ORDER[self.competition.discipline.name][x.name])
            return dances[-1]
        except KeyError:
            return self.dances[0]
        except IndexError:
            return self.dances[0]

    def has_dance(self, dance_id):
        return dance_id in [d.dance_id for d in self.dances]

    def has_dances(self):
        return len(self.dances) > 0

    def is_dance_active(self, dance):
        return [d for d in self.dance_active if d.dance == dance][0].is_active

    def dance_couples(self, dance):
        return [c for couples in [h.couples for h in self.heats if h.dance == dance] for c in couples]

    def number_of_heats(self, dance):
        return len([h for h in self.heats if h.dance == dance])

    def has_heats(self):
        return len(self.heats)

    def has_next_round(self):
        return any(r.round_id > self.round_id for r in self.competition.rounds)

    def adjudicator_marks(self, adjudicator, dance):
        marks = []
        for heat in self.heats:
            if heat.dance == dance:
                marks.extend([m for m in heat.marks if m.adjudicator == adjudicator])
        marks.sort(key=lambda x: x.couple.number)
        return marks

    def dance_lead_follow_list(self):
        lead_follow_list = {d.tag: {} for d in self.dances}
        for dance in self.dances:
            heats = [heat for heat in self.heats if heat.dance == dance]
            lead_follow = {couple.number: couple.follow.number for heat in heats for couple in heat.couples}
            follow_lead = {couple.follow.number: couple.number for heat in heats for couple in heat.couples}
            lead_follow_list[dance.tag].update(lead_follow)
            lead_follow_list[dance.tag].update(follow_lead)
        return lead_follow_list

    def dance_heat_list(self):
        dance_heats = {}
        for dance in self.dances:
            heats = [heat for heat in self.heats if heat.dance == dance]
            couple_heat = {couple.number: heat.number for heat in heats for couple in heat.couples}
            dance_heats.update({dance.tag: couple_heat})
        return dance_heats

    def adjudicator_mark_list(self):
        adjudicator_marks = [{'adjudicator': adjudicator.name,
                              'marks': {str(dance.dance_id): self.adjudicator_marks(adjudicator, dance)
                                        for dance in self.dances}}
                             for adjudicator in self.competition.adjudicators]
        return adjudicator_marks

    def split_couples_into_heats(self, heats):
        n = len(self.couples)
        k = heats
        if self.competition.mode == CompetitionMode.change_per_dance:
            couples = [c for c in create_couples_list(couples=self.couples)]
        else:
            couples = [c for c in self.couples]
        shuffle(couples)
        return [couples[i * (n // k) + min(i, n % k):(i + 1) * (n // k) + min(i + 1, n % k)] for i in range(k)]

    def create_heats(self, heats):
        for dance in self.dances:
            couples = self.split_couples_into_heats(heats)
            for idx, c in enumerate(couples, start=1):
                heat = Heat()
                heat.dance = dance
                heat.couples = c
                heat.number = idx
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
                        if current_app.config.get('ENV') == DEBUG_ENV:
                            mark.mark = random.choice([True, True, False])  # TESTING
                        heat.marks.append(mark)
        db.session.commit()

    def create_final(self):
        for dance in self.dances:
            heat = Heat()
            heat.dance = dance
            if self.competition.mode == CompetitionMode.change_per_dance:
                heat.couples = create_couples_list(couples=self.couples)
            else:
                heat.couples = self.couples
            heat.number = 1
            self.heats.append(heat)
            for adj in self.competition.adjudicators:
                if current_app.config.get('ENV') == DEBUG_ENV:
                    placings = list(range(1, len(heat.couples) + 1))  # TESTING
                for couple in heat.couples:
                    final_placing = FinalPlacing()
                    final_placing.adjudicator = adj
                    final_placing.couple = couple
                    final_placing.dance = dance
                    if current_app.config.get('ENV') == DEBUG_ENV:
                        # noinspection PyUnboundLocalVariable
                        final_placing.final_placing = random.choice(placings)  # TESTING
                        placings.remove(final_placing.final_placing)  # TESTING
                    self.final_placings.append(final_placing)
        db.session.commit()

    def get_cutoffs(self):
        round_result_list = [r.marks for r in self.round_results if r.marks != -1]
        round_result_list.sort()
        unique_results = list(set(round_result_list))
        unique_results.sort(reverse=True)
        return [(-1, f"all couples")] + [(r, f"{r} marks") for r in unique_results]

    def change_per_dance_dancers_rows(self):
        round_result_list = [r for r in self.marks()]
        leads = [c.lead for c in self.couples]
        follows = [c.follow for c in self.couples]
        results = {d: 0 for d in leads + follows}
        if self.type == RoundType.re_dance:
            directly_qualified_leads = [c for c in self.competition.leads if c not in leads]
            directly_qualified_follows = [c for c in self.competition.follows if c not in follows]
            results.update({d: -1 for d in directly_qualified_leads})
            results.update({d: -1 for d in directly_qualified_follows})
        for mark in round_result_list:
            results[mark.couple.lead] += 1 if mark.mark else 0
            results[mark.couple.follow] += 1 if mark.mark else 0
        dancers_list = [{'dancer': d, 'place': None, 'crosses': results[d], 'lead': d.role == LEAD,
                         'follow': d.role == FOLLOW, 'team': d.team} for d in results]
        dancers_list.sort(key=lambda x: (x['crosses'] != -1, -x['crosses'], not x['lead'], x['dancer'].number))
        unique_results = list(set([d['crosses'] for d in dancers_list]))
        unique_results.sort(key=lambda x: (x != -1, -x))
        result_placing = {}
        for i in unique_results:
            result_placing.update({i: [d['crosses'] for d in dancers_list].count(i)})
        result_map = {}
        counter = 1
        for i in unique_results:
            if result_placing[i] == 1:
                result_map.update({i: str(counter)})
            else:
                result_map.update({i: str(counter) + ' - ' + str(counter + result_placing[i] - 1)})
            counter += result_placing[i]
        for d in dancers_list:
            d['placing'] = result_map[d['crosses']]
        return dancers_list

    def get_cutoffs_for_change_per_dance(self):
        dancers_list = self.change_per_dance_dancers_rows()
        unique_results = list(set([d['crosses'] for d in dancers_list]))
        unique_results = [u for u in unique_results if u != -1]
        unique_results.sort(reverse=True)
        viable_unique_results = []
        for r in unique_results:
            dancers = [d for d in dancers_list if d['crosses'] >= r]
            if len([d for d in dancers if d['lead']]) == len([d for d in dancers if d['follow']]):
                viable_unique_results.append(r)
        return [(-1, f"all couples")] + [(r, f"{r} marks") for r in viable_unique_results]

    def adjudicator_dance_marks(self, adjudicator, dance):
        marks = list(itertools.chain.from_iterable([h.marks for h in self.heats if h.dance == dance]))
        return [m for m in marks if m.adjudicator == adjudicator]

    def adjudicator_dance_marked(self, adjudicator, dance):
        marks = self.adjudicator_dance_marks(adjudicator, dance)
        return [m for m in marks if m.adjudicator == adjudicator and m.mark]

    def adjudicator_dance_noted(self, adjudicator, dance):
        marks = self.adjudicator_dance_marks(adjudicator, dance)
        return [m for m in marks if m.adjudicator == adjudicator and m.notes > 0]

    def adjudicator_dance_placed(self, adjudicator, dance):
        placings = [p for p in self.final_placings if p.adjudicator == adjudicator and p.dance == dance]
        return [p for p in placings if p.final_placing in list(range(1, len(self.couples) + 1))]

    def adjudicator_dance_to_dict(self, adjudicator, dance):
        data = {
            'crossed': len(self.adjudicator_dance_marked(adjudicator, dance)),
            'couples': len(self.couples),
            'noted': len(self.adjudicator_dance_noted(adjudicator, dance)),
            'min_marks': self.min_marks,
            'max_marks': self.max_marks,
            'open': self.is_dance_active(dance),
        }
        return data

    def adjudicator_dance_final_to_dict(self, adjudicator, dance):
        data = {
            'placed': len(self.round.adjudicator_dance_placed(adjudicator, dance)),
            'couples': len(self.round.couples),
            'open': self.round.is_dance_active(self.dance),
        }
        return data

    def marks(self, dance=None):
        marks = []
        for heat in self.heats:
            if dance is not None:
                if heat.dance == dance:
                    for mark in heat.marks:
                        marks.append(mark)
            else:
                for mark in heat.marks:
                    marks.append(mark)
        return marks

    def has_one_heat(self):
        return len(self.dances) == len(self.heats)

    def dance_skating(self, dance):
        return SkatingDance(dancing_round=self, dance=dance)

    def skating_summary(self, follows=False):
        return SkatingSummary(dancing_round=self, follows=follows)

    def ranking_report(self, follows=False):
        return RankingReport(self.competition, follows=follows)

    def deactivate(self):
        for dance in self.dance_active:
            dance.is_active = False
        self.is_active = False
        db.session.commit()

    def is_place_given(self, adjudicator, dance, place):
        for placing in [p for p in self.final_placings if p.adjudicator == adjudicator and p.dance == dance]:
            if placing.final_placing == place:
                return True
        return False

    def adjudicators_present(self, dance):
        return [a for a in self.competition.adjudicators if a.round == self.round_id and a.dance == dance.dance_id]

    def adjudicators_missing(self, dance):
        return [a for a in self.competition.adjudicators
                if not a.round == self.round_id or not a.dance == dance.dance_id]

    def previous_rounds(self):
        return sorted([r for r in self.competition.rounds if r.round_id < self.round_id], key=lambda x: x.round_id,
                      reverse=True)

    def previous_rounds_dancers_rows(self):
        couples_placed = [c.number for c in self.couples]
        rounds = self.previous_rounds()
        total_results = []
        for r in rounds:
            round_results_list = [result for result in r.round_results if result.couple.number not in couples_placed]
            dancers_list = [{'result': r, 'placing': None, 'crosses': r.marks} for r in round_results_list]
            dancers_list.sort(key=lambda x: (-x['crosses'], x['result'].couple.number))
            unique_results = list(set([d['crosses'] for d in dancers_list]))
            unique_results.sort(reverse=True)
            result_placing = {}
            for i in unique_results:
                result_placing.update({i: [d['crosses'] for d in dancers_list].count(i)})
            result_map = {}
            counter = 1 + len(couples_placed)
            for i in unique_results:
                if result_placing[i] == 1:
                    result_map.update({i: str(counter)})
                else:
                    result_map.update({i: str(counter) + ' - ' + str(counter + result_placing[i] - 1)})
                counter += result_placing[i]
            for d in dancers_list:
                d['placing'] = result_map[d['crosses']]
            total_results.extend(dancers_list)
            couples_placed.extend([result.couple.number for result in r.round_results
                                   if result.couple.number not in couples_placed])
        return total_results

    def previous_rounds_change_per_dance_dancers_rows(self, leads_only=False, follows_only=False):
        leads_placed = [] if follows_only else [c.lead for c in self.couples]
        follows_placed = [] if leads_only else [c.follow for c in self.couples]
        dancers_placed = leads_placed + follows_placed
        rounds = self.previous_rounds()
        total_results = []
        for r in rounds:
            round_result_list = [m for m in r.marks()]
            leads = [c.lead for c in r.couples]
            follows = [c.follow for c in r.couples]
            results = {d: 0 for d in leads + follows}
            for mark in round_result_list:
                results[mark.couple.lead] += 1 if mark.mark else 0
                results[mark.couple.follow] += 1 if mark.mark else 0
            dancers_list = [{'dancer': d, 'place': None, 'crosses': results[d], 'lead': d.role == LEAD,
                             'follow': d.role == FOLLOW, 'team': d.team} for d in results if d not in dancers_placed]
            if leads_only:
                dancers_list = [d for d in dancers_list if d['lead']]
            if follows_only:
                dancers_list = [d for d in dancers_list if d['follow']]
            dancers_list.sort(key=lambda x: (x['crosses'] != -1, -x['crosses'], not x['lead'], x['dancer'].number))
            unique_results = list(set([d['crosses'] for d in dancers_list]))
            unique_results.sort(key=lambda x: (x != -1, -x))
            result_placing = {}
            for i in unique_results:
                result_placing.update({i: [d['crosses'] for d in dancers_list].count(i)})
            result_map = {}
            counter = 1 + len(dancers_placed)
            for i in unique_results:
                if result_placing[i] == 1:
                    result_map.update({i: str(counter)})
                else:
                    result_map.update({i: str(counter) + ' - ' + str(counter + result_placing[i] - 1)})
                counter += result_placing[i]
            for d in dancers_list:
                d['placing'] = result_map[d['crosses']]
            total_results.extend(dancers_list)
            dancers_placed.extend([d['dancer'] for d in dancers_list if d['dancer'] not in dancers_placed])
        return total_results

    def can_evaluate(self):
        for adjudicator in self.competition.adjudicators:
            for dance in self.dances:
                marks = [m.mark for m in self.adjudicator_marks(adjudicator, dance)]
                if True not in marks:
                    return False
        return True

    def evaluation_errors(self):
        errors_list = []
        for adjudicator in self.competition.adjudicators:
            for dance in self.dances:
                marks = [m.mark for m in self.adjudicator_marks(adjudicator, dance)]
                if True not in marks:
                    errors_list.append(f"{adjudicator} has zero marks in {dance}. This is probably an error.")
        return errors_list

    def no_re_dance_couples(self):
        previous_round = self.previous_round()
        if previous_round is not None:
            return [result.couple for result in self.round_results if result.marks == -1]

    def presenter_adjudicators(self):
        return list(sorted([{
            "id": a.adjudicator_id,
            "name": a.name,
            "present": a.is_present(self),
            "round": a.active_round(),
            "dance": a.active_dance()
        } for a in self.competition.adjudicators], key=lambda x: x["name"]))

    def leads(self):
        return [c.lead for c in self.couples]

    def follows(self):
        return [c.follow for c in self.couples]

    @staticmethod
    def presenter_dancers_list(couples=None, leads=None, follows=None):
        if couples is not None:
            return list(sorted([{"number": c.number, "name": c.names(), "team": c.teams()} for c in couples],
                               key=lambda x: x["number"]))
        if leads is not None and follows is not None:
            return {
                "leads": list(sorted([{"number": d.number, "name": d.name, "team": d.team}
                                      for d in leads], key=lambda x: x["number"])),
                "follows": list(sorted([{"number": d.number, "name": d.name, "team": d.team}
                                        for d in follows], key=lambda x: x["number"]))
            }

    def starting_list(self):
        if self.competition.mode in CHANGE_MODES:
            return self.presenter_dancers_list(leads=self.leads(), follows=self.follows())
        return self.presenter_dancers_list(couples=self.couples)

    def presenter_no_redance_couples(self):
        r = self.previous_round()
        if self.competition.mode in CHANGE_MODES:
            return self.presenter_dancers_list(leads=[d for d in r.leads() if d not in self.leads()],
                                               follows=[d for d in r.follows() if d not in self.follows()])
        return self.presenter_dancers_list(couples=[c for c in r.couples if c not in self.couples])

    def couples_present(self):
        couples = {d: {
            "name": d.name,
            "order": DANCE_ORDER[self.competition.discipline.name][d.name]
            if self.competition.discipline.name in DANCE_ORDER else self.competition.competition_id,
            "id": d.dance_id,
            "heats": []
        } for d in self.dances}
        for h in self.heats:
            couples[h.dance]["heats"].append({
                "number": h.number,
                "id": h.heat_id,
                "couples": list(sorted([{
                    "number": c.presenter_couple_number(),
                    "sort_number": c.couple.number,
                    "name": c.couple_name(),
                    "present": c.present
                } for c in h.couples_present], key=lambda x: x["sort_number"]))
            })
        return list(couples.values())

    def presenter_final_results(self):
        if self.competition.mode != CompetitionMode.change_per_dance:
            skating_couples = self.skating_summary()
            placings = {r.Index: r.Result for r in skating_couples.summary.itertuples()}
            couples = list(sorted([{
                "number": c.number,
                "name": c.names(),
                "lead": c.lead.name,
                "follow": c.follow.name,
                "team": c.teams(),
                "place": placings[c.number]
            } for c in self.couples], key=lambda x: x["place"]))
            return {
                "separate": False,
                "columns": list(skating_couples.summary.columns),
                "rows": [[c for c in r] for r in skating_couples.summary.itertuples()],
                "show_rules": skating_couples.show_rules,
                "dances": [d.tag for d in self.dances],
                "couples": couples,
                "rule10": {"rows": [[str(c) for c in r] for r in skating_couples.summary_rule_10.skating.itertuples()]},
                "rule11": {"rows": [[str(c) for c in r] for r in skating_couples.summary_rule_11.skating.itertuples()]}
            }
        leads = self.skating_summary()
        placings = {r.Index: r.Result for r in leads.summary.itertuples()}
        dancers = list(sorted([{
            "number": c.lead.number,
            "name": c.lead.name,
            "team": c.lead.team,
            "place": placings[c.lead.number]
        } for c in self.couples], key=lambda x: x["place"]))
        leads_data = {
            "columns": list(leads.summary.columns),
            "rows": [[c for c in r] for r in leads.summary.itertuples()],
            "show_rules": leads.show_rules,
            "dances": [d.tag for d in self.dances],
            "dancers": dancers,
            "rule10": {"rows": [[str(c) for c in r] for r in leads.summary_rule_10.skating.itertuples()]},
            "rule11": {"rows": [[str(c) for c in r] for r in leads.summary_rule_11.skating.itertuples()]}
        }
        follows = self.skating_summary(follows=True)
        placings = {r.Index: r.Result for r in follows.summary.itertuples()}
        dancers = list(sorted([{
            "number": c.follow.number,
            "name": c.follow.name,
            "team": c.follow.team,
            "place": placings[c.follow.number]
        } for c in self.couples], key=lambda x: x["place"]))
        follows_data = {
            "columns": list(follows.summary.columns),
            "rows": [[c for c in r] for r in follows.summary.itertuples()],
            "show_rules": follows.show_rules,
            "dances": [d.tag for d in self.dances],
            "dancers": dancers,
            "rule10": {"rows": [[str(c) for c in r] for r in follows.summary_rule_10.skating.itertuples()]},
            "rule11": {"rows": [[str(c) for c in r] for r in follows.summary_rule_11.skating.itertuples()]}
        }
        return {"separate": True, "leads": leads_data, "follows": follows_data}


class DanceActive(db.Model):
    __tablename__ = TABLE_DANCE_ACTIVE
    dance_active_id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.round_id', onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="dance_active")
    dance_id = db.Column(db.Integer, db.ForeignKey('dance.dance_id', onupdate="CASCADE", ondelete="CASCADE"))
    dance = db.relationship("Dance")

    def __repr__(self):
        return '{round} - {dance}'.format(round=self.round, dance=self.dance)


class Heat(db.Model):
    __tablename__ = TABLE_HEAT
    heat_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, default=1)
    floor = db.Column(db.Integer, default=1)
    round_id = db.Column(db.Integer, db.ForeignKey('round.round_id', onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="heats")
    dance_id = db.Column(db.Integer, db.ForeignKey('dance.dance_id'))
    dance = db.relationship("Dance")
    couples = db.relationship("Couple", secondary=heat_couple_table)
    marks = db.relationship("Mark", back_populates="heat", cascade='all, delete, delete-orphan')
    couples_present = db.relationship("CouplePresent", back_populates="heat", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return '{round} - {dance} - Heat {number}'.format(number=self.number, dance=self.dance, round=self.round)


class Mark(db.Model):
    __tablename__ = TABLE_MARK
    mark_id = db.Column(db.Integer, primary_key=True)
    mark = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Integer, default=0)
    adjudicator_id = db.Column(db.Integer, db.ForeignKey('adjudicator.adjudicator_id',
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    adjudicator = db.relationship("Adjudicator")
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    heat_id = db.Column(db.Integer, db.ForeignKey('heat.heat_id', onupdate="CASCADE", ondelete="CASCADE"))
    heat = db.relationship("Heat", back_populates="marks")

    def __repr__(self):
        return '{round} - {dance} - {adj} - {couple}'\
            .format(couple=self.couple, adj=self.adjudicator.name, dance=self.heat.dance, round=self.heat.round)

    def to_dict(self):
        data = {
            'marked': self.mark,
            'notes': self.notes,
            'crossed': len(self.heat.round.adjudicator_dance_marked(self.adjudicator, self.heat.dance)),
            'couples': len(self.heat.round.couples),
            'noted': len(self.heat.round.adjudicator_dance_noted(self.adjudicator, self.heat.dance)),
            'min_marks': self.heat.round.min_marks,
            'max_marks': self.heat.round.max_marks,
            'open': self.heat.round.is_dance_active(self.heat.dance),
        }
        return data


class FinalPlacing(db.Model):
    __tablename__ = TABLE_FINAL_PLACING
    final_placing_id = db.Column(db.Integer, primary_key=True)
    final_placing = db.Column(db.Integer, default=0)
    adjudicator_id = db.Column(db.Integer, db.ForeignKey('adjudicator.adjudicator_id',
                                                         onupdate="CASCADE", ondelete="CASCADE"))
    adjudicator = db.relationship("Adjudicator")
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    round_id = db.Column(db.Integer, db.ForeignKey('round.round_id', onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="final_placings")
    dance_id = db.Column(db.Integer, db.ForeignKey('dance.dance_id', onupdate="CASCADE", ondelete="CASCADE"))
    dance = db.relationship("Dance")

    def __repr__(self):
        return '{round} - {dance} - {adj} - {couple}'\
            .format(couple=self.couple, adj=self.adjudicator.name, dance=self.dance, round=self.round)

    def to_dict(self):
        data = {
            'place': self.final_placing,
            'placed': len(self.round.adjudicator_dance_placed(self.adjudicator, self.dance)),
            'couples': len(self.round.couples),
            'open': self.round.is_dance_active(self.dance),
        }
        return data


class CouplePresent(db.Model):
    __tablename__ = TABLE_COUPLE_PRESENT
    couple_present_id = db.Column(db.Integer, primary_key=True)
    present = db.Column(db.Boolean, default=False)
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    heat_id = db.Column(db.Integer, db.ForeignKey('heat.heat_id', onupdate="CASCADE", ondelete="CASCADE"))
    heat = db.relationship("Heat", back_populates="couples_present")

    def __repr__(self):
        return f"{self.heat.round} - {self.heat.dance} - {self.couple}"

    def presenter_couple_number(self):
        if self.heat.round.competition.mode in CHANGE_MODES:
            return f"{self.couple.lead.number} / {self.couple.follow.number}"
        return self.couple.number

    def couple_name(self):
        return f"{self.couple.lead.name} / {self.couple.follow.name}"


class RoundResult(db.Model):
    __tablename__ = TABLE_ROUND_RESULT
    round_result_id = db.Column(db.Integer, primary_key=True)
    couple_id = db.Column(db.Integer, db.ForeignKey('couple.couple_id', onupdate="CASCADE", ondelete="CASCADE"))
    couple = db.relationship("Couple")
    marks = db.Column(db.Integer, default=0)
    placing = db.Column(db.String(12))
    round_id = db.Column(db.Integer, db.ForeignKey('round.round_id', onupdate="CASCADE", ondelete="CASCADE"))
    round = db.relationship("Round", back_populates="round_results")

    def __repr__(self):
        return '{round} - {couple}'.format(couple=self.couple, round=self.round)
