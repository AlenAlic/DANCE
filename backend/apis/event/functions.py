from backend.models import db, active_event
from flask import current_app, g
from backend.constants import TOURNAMENT, XTDS, ODK, SOND, TAGS, BASE_DANCES, BONUS_DANCES, SECOND_BASE_DANCES, \
    XTDS_CLASSES, ODK_CLASSES, SOND_CLASSES, STANDARD, LATIN, BALLROOM_DISCIPLINES, STANDARD_DANCES, LATIN_DANCES, \
    TEST, BONUS, BEGINNERS, BREITENSPORT_QUALIFICATION, BREITENSPORT_COMPETITIONS, AMATEURS, PROFESSIONALS, MASTERS, \
    CHAMPIONS, CLOPEN_QUALIFICATION, CLOPEN_COMPETITIONS, CLOSED, OPEN_CLASS, \
    SLOW_WALTZ, TANGO, SLOW_FOXTROT, VIENNESE_WALTZ, QUICKSTEP, SAMBA, CHA_CHA_CHA, RUMBA, PASO_DOBLE, JIVE, \
    SALSA, BACHATA, MERENGUE, POLKA, \
    SOND_SENIOREN, ASPIRANTEN_JUNIOREN, NIEUWELINGEN_JUNIOREN, D_KLASSE_JUNIOREN, C_KLASSE_JUNIOREN,\
    B_KLASSE_JUNIOREN, A_KLASSE_JUNIOREN, OPEN_KLASSE_JUNIOREN, ASPIRANTEN_SENIOREN, NIEUWELINGEN_SENIOREN, \
    D_KLASSE_SENIOREN, C_KLASSE_SENIOREN, B_KLASSE_SENIOREN, A_KLASSE_SENIOREN, OPEN_KLASSE_SENIOREN, AL_ADJUDICATOR
from datetime import timedelta
from backend.models.event import Event
from backend.models.competition import Competition
from backend.models.competition.enums import CompetitionMode
from backend.models.dance import Dance
from backend.models.dancing_class import DancingClass
from backend.models.discipline import Discipline
from backend.models.user import User
from backend.models.adjudicator import Adjudicator
from backend.models.base import ADJUDICATOR_SYSTEM_TABLES


def create_base():
    create_base_dances()
    create_second_base_dances()
    create_dancing_classes()
    create_disciplines()


def create_base_dances():
    Dance.query.delete()
    db.session.commit()
    for d in BASE_DANCES:
        dance = Dance()
        dance.name = d["name"]
        dance.tag = d["tag"]
        dance.order = d["order"]
        db.session.add(dance)
    db.session.commit()
    if current_app.config.get(TOURNAMENT) == ODK:
        for d in BONUS_DANCES:
            dance = Dance()
            dance.name = d["name"]
            dance.tag = d["tag"]
            dance.order = d["order"]
            db.session.add(dance)
        db.session.commit()


def create_second_base_dances():
    for d in SECOND_BASE_DANCES:
        dance = Dance()
        dance.name = d["name"]
        dance.tag = d["tag"]
        dance.order = d["order"]
        db.session.add(dance)
    db.session.commit()


def create_dancing_classes():
    DancingClass.query.delete()
    db.session.commit()
    dancing_classes = XTDS_CLASSES
    if current_app.config.get(TOURNAMENT) == XTDS:
        dancing_classes = XTDS_CLASSES
    if current_app.config.get(TOURNAMENT) == ODK:
        dancing_classes = ODK_CLASSES
    elif current_app.config.get(TOURNAMENT) == SOND:
        dancing_classes = SOND_CLASSES
    for dc in dancing_classes:
        dancing_class = DancingClass()
        dancing_class.name = dc
        dancing_class.tag = TAGS[dc]
        db.session.add(dancing_class)
    db.session.commit()


def create_disciplines():
    Discipline.query.delete()
    db.session.commit()
    if current_app.config.get(TOURNAMENT) == ODK:
        for d in BASE_DANCES + BONUS_DANCES:
            discipline = Discipline()
            discipline.name = d["name"]
            discipline.tag = TAGS[d["name"]]
            db.session.add(discipline)
            db.session.commit()
            bonus = Discipline.query.filter(Discipline.name == d["name"]).first()
            bonus.dances.append(Dance.query.filter(Dance.name == d["name"]).first())
    else:
        for d in BALLROOM_DISCIPLINES:
            discipline = Discipline()
            discipline.name = d
            discipline.tag = TAGS[d]
            db.session.add(discipline)
            db.session.commit()
        ballroom = Discipline.query.filter(Discipline.name == STANDARD).first()
        ballroom.dances.extend(Dance.query.filter(Dance.name.in_(STANDARD_DANCES)).all())
        latin = Discipline.query.filter(Discipline.name == LATIN).first()
        latin.dances.extend(Dance.query.filter(Dance.name.in_(LATIN_DANCES)).all())
    db.session.commit()


def generate_xtds_competitions(time, competitions):
    create_xtds_competition(STANDARD, TEST, time)
    create_xtds_competition(LATIN, TEST, time)
    if AMATEURS in competitions or PROFESSIONALS in competitions \
            or MASTERS in competitions or CHAMPIONS in competitions:
        pass
        create_xtds_competition(STANDARD, BREITENSPORT_QUALIFICATION, time)
        create_xtds_competition(LATIN, BREITENSPORT_QUALIFICATION, time)
    for comp in competitions:
        create_xtds_competition(STANDARD, comp, time)
        create_xtds_competition(LATIN, comp, time)


def create_xtds_competition(disc, d_class, start_time):
    if disc == STANDARD and (d_class == CLOPEN_QUALIFICATION or d_class == CLOSED or d_class == OPEN_CLASS):
        start_time = start_time + timedelta(days=1)
    if disc == LATIN and d_class != CLOPEN_QUALIFICATION and d_class != CLOSED and d_class != OPEN_CLASS:
        start_time = start_time + timedelta(days=1)
    time = start_time
    c = Competition()
    c.discipline = Discipline.query.filter(Discipline.name == disc).first()
    c.dancing_class = DancingClass.query.filter(DancingClass.name == d_class).first()
    mode = CompetitionMode.single_partner
    floors = 1
    if d_class == TEST:
        c.test = True
        time = time + timedelta(hours=-1)
    if d_class == BREITENSPORT_QUALIFICATION:
        floors = 2
    if d_class == BEGINNERS:
        time = time + timedelta(minutes=40)
    if d_class == AMATEURS:
        time = time + timedelta(hours=1)
    if d_class == PROFESSIONALS:
        time = time + timedelta(hours=1, minutes=20)
    if d_class == MASTERS:
        time = time + timedelta(hours=1, minutes=40)
    if d_class == CHAMPIONS:
        time = time + timedelta(hours=2)
    if d_class == CLOPEN_QUALIFICATION:
        floors = 2
        mode = CompetitionMode.change_per_dance
        time = time + timedelta(hours=2, minutes=20)
    if d_class == CLOSED:
        mode = CompetitionMode.change_per_dance
        time = time + timedelta(hours=3)
    if d_class == OPEN_CLASS:
        mode = CompetitionMode.change_per_dance
        time = time + timedelta(hours=3, minutes=20)
    c.mode = mode
    c.floors = floors
    c.when = time
    c.event = g.event
    if d_class in BREITENSPORT_COMPETITIONS:
        c.qualification = Competition.query.join(DancingClass, Discipline)\
            .filter(DancingClass.name == BREITENSPORT_QUALIFICATION, Discipline.name == disc).first()
    if d_class in CLOPEN_COMPETITIONS:
        c.qualification = Competition.query.join(DancingClass, Discipline)\
            .filter(DancingClass.name == CLOPEN_QUALIFICATION, Discipline.name == disc).first()
    db.session.commit()


def generate_odk_competitions(time, competitions):
    create_odk_competition(SLOW_WALTZ, TEST, time)
    create_odk_competition(SAMBA, TEST, time)
    for comp in competitions:
        if comp in STANDARD_DANCES or comp in LATIN_DANCES:
            create_odk_competition(comp, BREITENSPORT_QUALIFICATION, time)
            create_odk_competition(comp, AMATEURS, time)
            create_odk_competition(comp, CHAMPIONS, time)
            create_odk_competition(comp, OPEN_CLASS, time)
        else:
            create_odk_competition(comp, BONUS, time)


def create_odk_competition(disc, d_class, start_time):
    start_time = start_time + timedelta(hours=1)
    if disc in LATIN_DANCES:
        start_time = start_time + timedelta(hours=5, minutes=30)
        if d_class == AMATEURS or d_class == CHAMPIONS or d_class == OPEN_CLASS:
            start_time = start_time + timedelta(minutes=30)
    time = start_time
    c = Competition()
    c.discipline = Discipline.query.filter(Discipline.name == disc).first()
    c.dancing_class = DancingClass.query.filter(DancingClass.name == d_class).first()
    c.mode = CompetitionMode.single_partner
    if d_class == TEST:
        c.test = True
        time = time + timedelta(hours=-1)
        if disc == SAMBA:
            time = time + timedelta(hours=-4, minutes=-30)
    if disc == SLOW_WALTZ or disc == SAMBA or disc == SALSA:
        time = time + timedelta(minutes=0)
    if disc == TANGO or disc == CHA_CHA_CHA or disc == BACHATA:
        time = time + timedelta(minutes=10)
    if disc == VIENNESE_WALTZ or disc == RUMBA or disc == MERENGUE:
        time = time + timedelta(minutes=20)
    if disc == SLOW_FOXTROT or disc == PASO_DOBLE:
        time = time + timedelta(minutes=30)
    if disc == QUICKSTEP or disc == JIVE:
        time = time + timedelta(minutes=40)
    if disc == POLKA:
        time = time + timedelta(minutes=50)
    if disc == SALSA or disc == BACHATA or disc == MERENGUE:
        time = time + timedelta(hours=6, minutes=30)
    if d_class == BREITENSPORT_QUALIFICATION:
        time = time + timedelta(minutes=0)
    if d_class == AMATEURS:
        time = time + timedelta(hours=1, minutes=0)
    if d_class == CHAMPIONS:
        time = time + timedelta(hours=1, minutes=5)
    if d_class == OPEN_CLASS:
        time = time + timedelta(hours=2, minutes=30)
    c.floors = 1
    c.when = time
    c.event = g.event
    if d_class in BREITENSPORT_COMPETITIONS:
        c.qualification = Competition.query.join(DancingClass, Discipline)\
            .filter(DancingClass.name == BREITENSPORT_QUALIFICATION, Discipline.name == disc).first()
    db.session.commit()


def generate_sond_competitions(time, competitions):
    create_sond_competition(STANDARD, TEST, time)
    create_sond_competition(LATIN, TEST, time)
    for comp in competitions:
        comp = comp.split("&")
        discipline = comp[0]
        dancing_class = comp[1]
        create_sond_competition(discipline, dancing_class, time)


def create_sond_competition(disc, d_class, start_time):
    start_time = start_time + timedelta(hours=1)
    if disc == LATIN:
        start_time = start_time + timedelta(hours=2)
    if d_class in SOND_SENIOREN:
        start_time = start_time + timedelta(hours=1)
    time = start_time
    c = Competition()
    c.discipline = Discipline.query.filter(Discipline.name == disc).first()
    c.dancing_class = DancingClass.query.filter(DancingClass.name == d_class).first()
    c.mode = CompetitionMode.single_partner
    floors = 1
    if d_class == TEST:
        c.test = True
        time = time + timedelta(hours=-1)
    if d_class == ASPIRANTEN_JUNIOREN or d_class == ASPIRANTEN_SENIOREN:
        time = time + timedelta(minutes=0)
    if d_class == NIEUWELINGEN_JUNIOREN or d_class == NIEUWELINGEN_SENIOREN:
        time = time + timedelta(minutes=10)
    if d_class == D_KLASSE_JUNIOREN or d_class == D_KLASSE_SENIOREN:
        time = time + timedelta(minutes=20)
    if d_class == C_KLASSE_JUNIOREN or d_class == C_KLASSE_SENIOREN:
        time = time + timedelta(minutes=30)
    if d_class == B_KLASSE_JUNIOREN or d_class == B_KLASSE_SENIOREN:
        time = time + timedelta(minutes=40)
    if d_class == A_KLASSE_JUNIOREN or d_class == A_KLASSE_SENIOREN:
        time = time + timedelta(minutes=50)
    if d_class == OPEN_KLASSE_JUNIOREN or d_class == OPEN_KLASSE_SENIOREN:
        time = time + timedelta(hours=1)
    c.floors = floors
    c.when = time
    c.event = g.event
    db.session.commit()


def reset_db():
    meta = db.metadata
    Competition.query.delete()
    Adjudicator.query.delete()
    e = active_event()
    if e is not None:
        if len(e.results) == 0:
            db.session.delete(e)
    Event.query.update({Event.is_active: False}, synchronize_session="fetch")
    User.query.filter(User.access == AL_ADJUDICATOR).delete()
    for table in reversed(meta.sorted_tables):
        if table.name in ADJUDICATOR_SYSTEM_TABLES:
            print('Cleared table {}.'.format(table))
            db.session.execute(table.delete())
            db.session.execute("ALTER TABLE {} AUTO_INCREMENT = 1;".format(table.name))
    db.session.commit()
