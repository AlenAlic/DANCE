from flask import request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, BooleanField, DateField, \
    IntegerField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
import wtforms_sqlalchemy.fields as f
from adjudication_system.models import DancingClass, Discipline, Competition, RoundType, Couple, Adjudicator, \
    Dance, Dancer, CompetitionMode
import datetime as dt
from adjudication_system.values import *
from contextlib import suppress
from adjudication_system.adjudication_system.validators import UniqueDancer, EqualNumberLeadsFollows, \
    UniqueDancerEdit, UniqueDancerCompetition, UniqueCompetitionDancer, UniquePerson


def get_pk_from_identity(obj):
    cls, key = f.identity_key(instance=obj)[:2]
    return ':'.join(f.text_type(x) for x in key)


f.get_pk_from_identity = get_pk_from_identity


class DancerForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.number.data = max([d.number for d in Dancer.query.all()] + [0]) + 1

    name = StringField('Name', validators=[DataRequired()])
    role = SelectField('Role', validators=[DataRequired()], choices=[("", ""), (LEAD, LEAD), (FOLLOW, FOLLOW)])
    number = IntegerField('Number')
    team = StringField('Team', validators=[DataRequired()])
    submit = SubmitField('Create dancer')


class EditDancerForm(FlaskForm):
    def __init__(self, dancer, **kwargs):
        super().__init__(**kwargs)
        self.dancer = dancer
        self.name.data = dancer.name
        self.role.data = dancer.role
        self.number.data = dancer.number
        self.team.data = dancer.team
        self.partners.data = ', '.join(["{p0} ({p1})".format(p0=p[0], p1=', '.join(['{}'.format(d) for d in p[1]]))
                                        for p in dancer.partners()])
        self.competitions.choices = [(c.competition_id, c) for c in Competition.query.join(
            DancingClass, Competition.dancing_class_id == DancingClass.dancing_class_id)
            .filter(DancingClass.name != TEST, Competition.mode != CompetitionMode.single_partner)
            .all() if c.qualification is None and not c.has_rounds()]
        if request.method == GET:
            self.competitions.data = [c.competition_id for c in dancer.competitions()]

    name = StringField('Name', validators=[DataRequired()])
    role = StringField('Role')
    number = StringField('Number')
    team = StringField('Team', validators=[DataRequired()])
    partners = StringField('Partners')
    competitions = SelectMultipleField(label="Competitions", validators=[UniqueCompetitionDancer()],
                                       coerce=int, render_kw={'data-role': 'select2'})


class ImportDancersForm(FlaskForm):
    import_string = TextAreaField(label="Import from CSV string (number,name,is_lead,is_follow), where the is_lead "
                                        "and is_follow columns are either TRUE or FALSE", validators=[DataRequired()],
                                  render_kw={"style": "resize:none", "rows": "4"})
    import_submit = SubmitField('Import from string')


class CoupleForm(FlaskForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lead.query = Dancer.query.filter(Dancer.role == LEAD).order_by(Dancer.name)
        self.follow.query = Dancer.query.filter(Dancer.role == FOLLOW).order_by(Dancer.name)
        self.competitions.choices = [(c.competition_id, c) for c in Competition.query.join(
            DancingClass, Competition.dancing_class_id == DancingClass.dancing_class_id)
            .filter(DancingClass.name != TEST, Competition.mode == CompetitionMode.single_partner)
            .all() if c.qualification is None and not c.has_rounds()]

    lead = QuerySelectField('Lead', validators=[DataRequired(), UniquePerson()], render_kw={'data-role': 'select2'},
                            allow_blank=True, blank_text='Please select a lead for the couple.')
    follow = QuerySelectField('Follow', validators=[DataRequired(), UniquePerson()], render_kw={'data-role': 'select2'},
                              allow_blank=True, blank_text='Please select a follow for the couple.')
    competitions = SelectMultipleField(label="Competitions", validators=[DataRequired(), UniqueDancer()], coerce=int,
                                       render_kw={'data-role': 'select2'})
    submit = SubmitField('Create couple')


class EditCoupleForm(CoupleForm):
    def __init__(self, couple=None, **kwargs):
        super().__init__(**kwargs)
        if couple is not None:
            self.number.data = couple.number
            self.lead.data = couple.lead
            self.follow.data = couple.follow
            self.couple = couple
            if request.method == GET:
                self.competitions.data = [c.competition_id for c in couple.competitions]

    number = StringField('Number')
    lead = StringField('Lead')
    follow = StringField('Follow')
    competitions = SelectMultipleField(label="Competitions", validators=[DataRequired(), UniqueDancerEdit()],
                                       coerce=int, render_kw={'data-role': 'select2'})


class SplitForm(FlaskForm):
    def __init__(self, split_couples, **kwargs):
        super().__init__(**kwargs)
        self.scenarios.choices = [(k, k) for k in split_couples]

    scenarios = SelectField('Scenarios', validators=[DataRequired()])
    submit = SubmitField('Split')


class DanceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], description="Slow Waltz, Tango, etc.")
    tag = StringField('Tag', validators=[DataRequired()], description="SW, TG, etc.")
    dance_submit = SubmitField('Create Dance')


class DisciplineForm(FlaskForm):
    def __init__(self, discipline=None, **kwargs):
        super().__init__(**kwargs)
        self.dances.choices = [(d.dance_id, d.name) for d in Dance.query.filter(Dance.discipline_id.is_(None)).all()]
        if discipline is not None:
            self.dances.choices.extend([(d.dance_id, d.name) for d in discipline.dances])
            if request.method == "GET":
                self.name.data = discipline.name
                self.dances.data = [d.dance_id for d in discipline.dances]

    name = StringField('Name', validators=[DataRequired()], description="Usually Ballroom or Latin")
    dances = SelectMultipleField(label="Dances", validators=[DataRequired()], render_kw={'data-role': 'select2'},
                                 coerce=int, description="Dances that belong to this discipline")
    discipline_submit = SubmitField('Create Discipline')


class DancingClassForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()],
                       description="{qualification}, {amateurs}, {open_class}, etc."
                       .format(qualification=BREITENSPORT_QUALIFICATION, amateurs=AMATEURS, open_class=OPEN_CLASS))
    dancing_class_submit = SubmitField('Create Class')


class CreateAdjudicatorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    adjudicator_contestant_submit = SubmitField('Create adjudicator')


class EventForm(FlaskForm):
    name = StringField('Event name', validators=[DataRequired()])
    event_submit = SubmitField('Create Event')


class CompetitionForm(FlaskForm):
    def __init__(self, comp=None, **kwargs):
        super().__init__(**kwargs)
        self.dancing_class.query = DancingClass.query
        self.discipline.query = Discipline.query
        self.qualification.query = Competition.query
        self.adjudicators.choices = [(a.adjudicator_id, a) for a in Adjudicator.query.order_by(Adjudicator.name).all()]
        self.competition_couples.choices = sorted([(c.couple_id, c) for c in Couple.query.all()],
                                                  key=lambda x: x[1].number)
        self.competition_leads.choices = [(d.dancer_id, d) for d in Dancer.query.order_by(Dancer.name).all()
                                          if d.role == LEAD]
        self.competition_follows.choices = [(d.dancer_id, d) for d in Dancer.query.order_by(Dancer.name).all()
                                            if d.role == FOLLOW]
        if comp is not None:
            self.qualification.query = self.qualification.query \
                .filter(Competition.competition_id != comp.competition_id)
            if request.method == "GET":
                self.dancing_class.data = comp.dancing_class
                self.discipline.data = comp.discipline
                self.floors.data = comp.floors
                self.when.data = comp.when
                self.qualification.data = comp.qualification
                with suppress(AttributeError):
                    self.mode.data = comp.mode.name
                self.adjudicators.data = [a.adjudicator_id for a in comp.adjudicators]
                self.competition_couples.data = [c.couple_id for c in comp.couples]
                self.competition_leads.data = [d.dancer_id for d in comp.leads]
                self.competition_follows.data = [d.dancer_id for d in comp.follows]
                if current_app.config.get('ENV') == DEBUG_ENV:
                    if len(comp.couples) == 0 and len(comp.leads) == 0 and len(comp.follows) == 0:
                        all_couples = [c.couple_id for c in Couple.query.all()]  # TESTING
                        if comp.dancing_class.name == TEST:  # TESTING
                            self.competition_couples.data = all_couples[0:12]
                        if comp.dancing_class.name == BEGINNERS:  # TESTING
                            self.competition_couples.data = all_couples[0:40]  # TESTING
                        if comp.dancing_class.name == BREITENSPORT_QUALIFICATION:  # TESTING
                            self.competition_couples.data = all_couples[40:200]  # TESTING
                        if comp.dancing_class.name == CLOSED:  # TESTING
                            self.competition_couples.data = all_couples[200:270]  # TESTING
                        if comp.dancing_class.name == OPEN_CLASS:  # TESTING
                            self.competition_couples.data = all_couples[270:300]  # TESTING
                    if len(comp.couples) == 0 and len(comp.leads) == 0 and len(comp.follows) == 0:
                        all_leads = [d.dancer_id for d in Dancer.query.all() if d.role == LEAD]
                        if comp.dancing_class.name == BEGINNERS:  # TESTING
                            self.competition_leads.data = all_leads[0:40]  # TESTING
                        if comp.dancing_class.name == BREITENSPORT_QUALIFICATION:  # TESTING
                            self.competition_leads.data = all_leads[40:200]  # TESTING
                        if comp.dancing_class.name == CLOSED:  # TESTING
                            self.competition_leads.data = all_leads[200:270]  # TESTING
                        if comp.dancing_class.name == OPEN_CLASS:  # TESTING
                            self.competition_leads.data = all_leads[270:300]  # TESTING
                    if len(comp.couples) == 0 and len(comp.leads) == 0 and len(comp.follows) == 0:
                        all_follows = [d.dancer_id for d in Dancer.query.all() if d.role == FOLLOW]
                        if comp.dancing_class.name == BEGINNERS:  # TESTING
                            self.competition_follows.data = all_follows[0:40]  # TESTING
                        if comp.dancing_class.name == BREITENSPORT_QUALIFICATION:  # TESTING
                            self.competition_follows.data = all_follows[40:200]  # TESTING
                        if comp.dancing_class.name == CLOSED:  # TESTING
                            self.competition_follows.data = all_follows[200:270]  # TESTING
                        if comp.dancing_class.name == OPEN_CLASS:  # TESTING
                            self.competition_follows.data = all_follows[270:300]  # TESTING

    dancing_class = QuerySelectField('Class', validators=[DataRequired()], allow_blank=True, blank_text="",
                                     description="{qualification}, {amateurs}, {open_class}, etc."
                                     .format(qualification=BREITENSPORT_QUALIFICATION, amateurs=AMATEURS,
                                             open_class=OPEN_CLASS))
    discipline = QuerySelectField('Discipline', validators=[DataRequired()], allow_blank=True, blank_text="",
                                  description="Usually Ballroom or Latin")
    qualification = QuerySelectField('Qualification', allow_blank=True, blank_text="",
                                     description="Indicates if this competition is the result of a qualification "
                                                 "round being split up into several competitions. Leave blank if "
                                                 "this is not the case.")
    floors = SelectField('Floors', choices=[(i, i) for i in [1, 2, 3, 4, 5]], coerce=int,
                         description="The maximum number of floors that can be used during this competition.")
    when = DateTimeField('Date/Time', default=dt.datetime.now(),
                         description="The time is used to sort the competitions in the menu on the left.")
    adjudicators = SelectMultipleField(label="Adjudicators", coerce=int, render_kw={'data-role': 'select2'})
    competition_couples = SelectMultipleField(label="Couples", render_kw={'data-role': 'select2'}, coerce=int,
                                              validators=[UniqueDancerCompetition()])
    competition_leads = SelectMultipleField(label="Leads", render_kw={'data-role': 'select2'}, coerce=int)
    competition_follows = SelectMultipleField(label="Follows", render_kw={'data-role': 'select2'}, coerce=int)
    mode = SelectField('Mode', validators=[DataRequired()], choices=[(e.name, e.value) for e in CompetitionMode],
                       default=CompetitionMode.single_partner.name,
                       description="Mode of the competition in terms of partnering.")
    comp_submit = SubmitField('Create Competition')


class DefaultCompetitionForm(FlaskForm):
    beginners = BooleanField(BEGINNERS)
    amateurs = BooleanField(AMATEURS)
    professionals = BooleanField(PROFESSIONALS)
    masters = BooleanField(MASTERS)
    champions = BooleanField(CHAMPIONS)
    closed = BooleanField(CLOSED)
    open_class = BooleanField(OPEN_CLASS)
    when = DateField('Start date', default=dt.datetime.now(), description='Start date of the event (the Saturday)',
                     render_kw={"type": "date"})
    default_submit = SubmitField('Create default competitions')


class BaseRoundForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                       description="Type of round, first round, qualification, re-dance, etc.")
    min_marks = IntegerField('', render_kw={'style': 'width:4rem;', 'type': "number", 'min': 1, 'step': 1})
    max_marks = IntegerField('', render_kw={'style': 'width:4rem;', 'type': "number", 'min': 1, 'step': 1})
    heats = IntegerField('Heats', default=1, render_kw={'style': 'width:4rem;', 'type': "number", 'min': 1, 'step': 1})
    dances = SelectMultipleField(label="Dances", validators=[DataRequired()], render_kw={'data-role': 'select2'},
                                 coerce=int)


class CreateFirstRoundForm(BaseRoundForm):
    def __init__(self, comp, **kwargs):
        super().__init__(**kwargs)
        self.competition = comp
        self.type.choices = [(e.name, e.value) for e in RoundType if e in
                             [RoundType.qualification, RoundType.general_look, RoundType.first_round]]
        self.min_marks.render_kw.update({'max': comp.max_couples()})
        self.min_marks.validators = [NumberRange(min=1, max=comp.max_couples())]
        self.max_marks.render_kw.update({'max': comp.max_couples()})
        self.max_marks.validators = [NumberRange(min=1, max=comp.max_couples())]
        self.heats.render_kw.update({'max': comp.max_couples()})
        self.heats.validators = [NumberRange(min=1, max=comp.max_couples())]
        self.dances.choices = [(d.dance_id, d) for d in comp.discipline.dances]
        self.dances.validators = [DataRequired(), EqualNumberLeadsFollows()]
        if request.method == "GET":
            self.min_marks.data = min(int(comp.max_couples() / 2), 1)
            self.max_marks.data = min(int(comp.max_couples() / 2), 1)
            if comp.discipline.name in BASIC_DANCES:
                self.dances.data = [d.dance_id for d in comp.discipline.dances
                                    if d.name in BASIC_DANCES[comp.discipline.name]]
        if comp.dancing_class.name == BREITENSPORT_QUALIFICATION:
            self.type.choices = [(RoundType.qualification.name, RoundType.qualification.value)]
        if request.method == "GET":
            if comp.dancing_class.name != BREITENSPORT_QUALIFICATION:
                self.type.data = RoundType.first_round.name

    round_submit = SubmitField('Create round')


class ConfigureNextRoundForm(BaseRoundForm):
    def __init__(self, dancing_round, **kwargs):
        super().__init__(**kwargs)
        if dancing_round.is_re_dance():
            couples_max = dancing_round.competition.max_couples()
        else:
            couples_max = len(dancing_round.couples)
        self.min_marks.render_kw.update({'max': couples_max})
        self.min_marks.validators = [NumberRange(min=1, max=couples_max)]
        self.max_marks.render_kw.update({'max': couples_max})
        self.max_marks.validators = [NumberRange(min=1, max=couples_max)]
        self.heats.render_kw.update({'max': couples_max})
        self.heats.validators = [NumberRange(min=1, max=couples_max)]
        self.dances.choices = [(d.dance_id, d) for d in dancing_round.competition.discipline.dances]
        if dancing_round.competition.is_change_per_dance():
            self.cutoff.choices = dancing_round.get_cutoffs_for_change_per_dance()
        else:
            self.cutoff.choices = dancing_round.get_cutoffs()
        if request.method == "GET":
            self.min_marks.data = min(int(couples_max / 2), 1)
            self.max_marks.data = min(int(couples_max / 2), 1)
            if dancing_round.competition.discipline.name in BASIC_DANCES:
                if dancing_round.is_completed():
                    self.dances.data = [d.dance_id for d in dancing_round.dances]
                else:
                    self.dances.data = [d.dance_id for d in dancing_round.competition.discipline.dances
                                        if d.name in BASIC_DANCES[dancing_round.competition.discipline.name]]
                if len(dancing_round.heats) == 0:
                    self.type.data = dancing_round.type.name
        if dancing_round.first_round_after_qualification_split():
            self.cutoff.data = 0
        self.type.choices = [("", "")] + [(e.name, e.value) for e in RoundType if e.name != RoundType.second_round.name]
        if dancing_round.is_general_look() or dancing_round.is_qualification() or dancing_round.is_first_round():
            self.type.choices = [("", "")] + [(e.name, e.value) for e in RoundType if e
                                              in [RoundType.re_dance,  # RoundType.second_round,
                                                  RoundType.intermediate_round, RoundType.semi_final, RoundType.final]]
        if dancing_round.is_re_dance() or dancing_round.is_second_round() or dancing_round.is_intermediate_round():
            self.type.choices = [("", "")] + [(e.name, e.value) for e in RoundType if e
                                              in [RoundType.intermediate_round, RoundType.semi_final, RoundType.final]]
        if dancing_round.is_semi_final():
            self.type.choices = [("", "")] + [(e.name, e.value) for e in RoundType if e
                                              in [RoundType.semi_final, RoundType.final]]
            if request.method == "GET":
                self.min_marks.data = 1
                self.max_marks.data = 1
                self.heats.data = 1
        if dancing_round.is_final():
            self.type.choices = [(RoundType.final.name, RoundType.final.value)]

    cutoff = SelectField('Cutoff for next round', validators=[DataRequired()], coerce=int)
    round_submit = SubmitField('Create round')


COPIES_RENDER = {'style': 'width:4rem;', 'type': "number", 'min': 1, 'step': 1}


class PrintReportsForm(FlaskForm):
    heats_by_number = BooleanField('Heats by starting No.')
    heats_by_number_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    heats_by_dance = BooleanField('Heats by dance')
    heats_by_dance_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    qualified_starts = BooleanField('Qualified starts')
    qualified_starts_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    adjudication_sheets = BooleanField('Adjudication sheets')
    adjudication_sheets_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    placings_after_round = BooleanField('Placings after round')
    placings_after_round_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    final_evaluation = BooleanField('Evaluation of final')
    final_evaluation_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    tournament_result = BooleanField('Competition results')
    tournament_result_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    ranking_report = BooleanField('Ranking report')
    ranking_report_copies = IntegerField('', default=1, render_kw=COPIES_RENDER)
    print_submit = SubmitField('Print')
    show_submit = SubmitField('Show')

    def something_to_print(self):
        return self.heats_by_number.data or self.heats_by_dance.data or self.qualified_starts.data \
               or self.adjudication_sheets.data or self.placings_after_round.data or self.final_evaluation.data \
               or self.tournament_result.data or self.ranking_report.data
