from flask import render_template, redirect, url_for, flash, request, g, Markup, current_app
from flask_login import login_required, current_user
from adjudication_system import db
from adjudication_system.adjudication_system import bp
from adjudication_system.adjudication_system.forms import SplitForm, EventForm, CompetitionForm, \
    CreateFirstRoundForm, DefaultCompetitionForm, ConfigureNextRoundForm, DanceForm, DisciplineForm, DancingClassForm, \
    PrintReportsForm, CoupleForm, EditCoupleForm, EditDancerForm, CreateAdjudicatorForm, DancerForm, ImportDancersForm,\
    ImportCouplesForm
from adjudication_system.models import User, Event, Competition, DancingClass, Discipline, Dance, Round, \
    RoundType, Adjudicator, Couple, CouplePresent, RoundResult, DanceActive, Dancer, CompetitionMode, \
    create_couples_list, ADJUDICATOR_SYSTEM_TABLES, requires_access_level
from itertools import combinations
from adjudication_system.values import *
from datetime import datetime, timedelta
import statistics
from sqlalchemy import or_
from adjudication_system.skating import generate_placings


def reset():
    meta = db.metadata
    Competition.query.delete()
    Event.query.delete()
    User.query.filter(User.adjudicator_id.isnot(None)).delete()
    for table in reversed(meta.sorted_tables):
        if table.name in ADJUDICATOR_SYSTEM_TABLES:
            print('Cleared table {}.'.format(table))
            db.session.execute(table.delete())
            db.session.execute("ALTER TABLE {} AUTO_INCREMENT = 1;".format(table.name))
    db.session.commit()


def create_adjudicators():
    for adj in ADJUDICATORS:
        adjudicator = Adjudicator()
        adjudicator.name = adj['name']
        adjudicator.tag = adj['tag']
        user = User()
        user.username = adjudicator.tag
        user.set_password(adjudicator.tag)
        user.is_active = True
        user.access = ACCESS[ADJUDICATOR]
        user.adjudicator = adjudicator
        db.session.add(user)
        db.session.commit()


def create_couples():
    for c in COUPLES:
        lead = Dancer()
        lead.name = c['lead']
        lead.role = LEAD
        lead.team = c['lead_team']
        lead.number = c['number']
        db.session.add(lead)
        follow = Dancer()
        follow.name = c['follow']
        follow.role = FOLLOW
        follow.team = c['follow_team']
        follow.number = c['number'] + len(COUPLES) + 200
        db.session.add(follow)
        couple = Couple()
        couple.number = lead.number
        couple.lead = lead
        couple.follow = follow
        db.session.add(couple)
        db.session.commit()


def create_dances():
    Dance.query.delete()
    db.session.commit()
    for d in DANCES:
        dance = Dance()
        dance.name = d["name"]
        dance.tag = d["tag"]
        db.session.add(dance)
        db.session.commit()
    if current_app.config.get(ODK):
        for d in BONUS_DANCES:
            dance = Dance()
            dance.name = d["name"]
            dance.tag = d["tag"]
            db.session.add(dance)
            db.session.commit()


def create_dancing_classes():
    DancingClass.query.delete()
    db.session.commit()
    if not current_app.config.get(ODK):
        for dc in DANCING_CLASSES:
            dancing_class = DancingClass()
            dancing_class.name = dc
            db.session.add(dancing_class)
            db.session.commit()
    else:
        for dc in ODK_CLASSES:
            dancing_class = DancingClass()
            dancing_class.name = dc
            db.session.add(dancing_class)
            db.session.commit()


def create_disciplines():
    Discipline.query.delete()
    db.session.commit()
    if not current_app.config.get(ODK):
        for d in ALL_COMPETITIONS:
            discipline = Discipline()
            discipline.name = d
            db.session.add(discipline)
            db.session.commit()
        ballroom = Discipline.query.filter(Discipline.name == BALLROOM).first()
        ballroom.dances.extend(Dance.query.filter(Dance.name.in_(BALLROOM_DANCES)).all())
        latin = Discipline.query.filter(Discipline.name == LATIN).first()
        latin.dances.extend(Dance.query.filter(Dance.name.in_(LATIN_DANCES)).all())
    else:
        for d in DANCES + BONUS_DANCES:
            db.session.add(Discipline(name=d['name']))
            db.session.commit()
            bonus = Discipline.query.filter(Discipline.name == d['name']).first()
            bonus.dances.append(Dance.query.filter(Dance.name == d['name']).first())
    db.session.commit()


def create_base():
    create_dances()
    create_dancing_classes()
    create_disciplines()
    db.session.commit()


@bp.route('/event', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def event():
    event_form = EventForm()
    competition_form = CompetitionForm()
    default_form = DefaultCompetitionForm()
    if event_form.event_submit.name in request.form:
        if event_form.validate_on_submit():
            e = Event()
            e.name = event_form.name.data
            db.session.add(e)
            db.session.commit()
            flash("Created {} event.".format(e.name))
            return redirect(url_for('adjudication_system.event'))
    if competition_form.comp_submit.name in request.form:
        if competition_form.validate_on_submit():
            c = Competition()
            c.discipline = competition_form.discipline.data
            c.dancing_class = competition_form.dancing_class.data
            c.floors = competition_form.floors.data
            c.when = competition_form.when.data
            c.event = g.event
            db.session.commit()
            flash("Created {} competition.".format(c))
            return redirect(url_for('adjudication_system.event'))
    if default_form.default_submit.name in request.form:
        if default_form.validate_on_submit():
            create_base()
            start_time = datetime(default_form.when.data.year, default_form.when.data.month,
                                  default_form.when.data.day, 9, 0, 0)
            if not current_app.config.get(ODK):
                create_default_competition(BALLROOM, TEST, start_time)
                if default_form.beginners.data:
                    create_default_competition(BALLROOM, BEGINNERS, start_time)
                    create_default_competition(LATIN, BEGINNERS, start_time)
                if default_form.amateurs.data or default_form.professionals.data or \
                        default_form.masters.data or default_form.champions.data:
                    create_default_competition(BALLROOM, BREITENSPORT_QUALIFICATION, start_time)
                    create_default_competition(LATIN, BREITENSPORT_QUALIFICATION, start_time)
                if default_form.amateurs.data:
                    create_default_competition(BALLROOM, AMATEURS, start_time)
                    create_default_competition(LATIN, AMATEURS, start_time)
                if default_form.professionals.data:
                    create_default_competition(BALLROOM, PROFESSIONALS, start_time)
                    create_default_competition(LATIN, PROFESSIONALS, start_time)
                if default_form.masters.data:
                    create_default_competition(BALLROOM, MASTERS, start_time)
                    create_default_competition(LATIN, MASTERS, start_time)
                if default_form.champions.data:
                    create_default_competition(BALLROOM, CHAMPIONS, start_time)
                    create_default_competition(LATIN, CHAMPIONS, start_time)
                if default_form.closed.data:
                    create_default_competition(BALLROOM, CLOSED, start_time)
                    create_default_competition(LATIN, CLOSED, start_time)
                if default_form.open_class.data:
                    create_default_competition(BALLROOM, OPEN_CLASS, start_time)
                    create_default_competition(LATIN, OPEN_CLASS, start_time)
            else:
                generate_odk_competitions(start_time)
            flash("Created base dances, disciplines, classes, and the chosen default competitions.")
            return redirect(url_for('adjudication_system.event'))
    form = request.args
    if 'reset' in form:
        reset()
        flash('Tables reset')
    if "populate_test" in form:
        if len(Couple.query.all()) > 0 and len(Adjudicator.query.all()) > 0:
            flash('Couples and adjudicators already present. Did not import dummy data', "alert-warning")
        if len(Couple.query.all()) == 0:
            create_couples()
            flash('Populated with dummy couples')
        if len(Adjudicator.query.all()) == 0:
            create_adjudicators()
            flash('Populated with dummy adjudicators')
    if len(form) > 0:
        return redirect(url_for('adjudication_system.event'))
    return render_template('adjudication_system/event.html', event_form=event_form, competition_form=competition_form,
                           default_form=default_form)


def create_default_competition(disc, d_class, start_time):
    if disc == BALLROOM and (d_class == CLOSED or d_class == OPEN_CLASS):
        start_time = start_time + timedelta(days=1)
    if disc == LATIN and d_class != CLOSED and d_class != OPEN_CLASS:
        start_time = start_time + timedelta(days=1)
    time = start_time
    c = Competition()
    c.discipline = Discipline.query.filter(Discipline.name == disc).first()
    c.dancing_class = DancingClass.query.filter(DancingClass.name == d_class).first()
    c.mode = CompetitionMode.single_partner
    floors = 1
    if d_class == TEST:
        time = time + timedelta(hours=-1)
    if d_class == BREITENSPORT_QUALIFICATION:
        floors = 2
        time = time + timedelta(hours=1)
    if d_class == AMATEURS:
        time = time + timedelta(hours=2)
    if d_class == PROFESSIONALS:
        time = time + timedelta(hours=3)
    if d_class == MASTERS:
        time = time + timedelta(hours=4)
    if d_class == CHAMPIONS:
        time = time + timedelta(hours=5)
    if d_class == CLOSED:
        time = time + timedelta(hours=6)
    if d_class == OPEN_CLASS:
        time = time + timedelta(hours=7)
    c.floors = floors
    c.when = time
    c.event = g.event
    if d_class in BREITENSPORT_COMPETITIONS:
        c.qualification = Competition.query.join(DancingClass, Discipline)\
            .filter(DancingClass.name == BREITENSPORT_QUALIFICATION, Discipline.name == disc).first()
    db.session.commit()


def generate_odk_competitions(time):
    create_odk_competition(SLOW_WALTZ, TEST, time)
    for d in DANCES + BONUS_DANCES:
        if d['name'] in BALLROOM_DANCES or d['name'] in LATIN_DANCES:
            create_odk_competition(d['name'], BREITENSPORT_QUALIFICATION, time)
            create_odk_competition(d['name'], AMATEURS, time)
            create_odk_competition(d['name'], CHAMPIONS, time)
            create_odk_competition(d['name'], OPEN_CLASS, time)
        else:
            create_odk_competition(d['name'], BONUS, time)


def create_odk_competition(disc, d_class, start_time):
    if disc in BALLROOM_DANCES:
        pass
    elif disc in LATIN_DANCES:
        start_time = start_time + timedelta(days=1)
    else:
        start_time = start_time + timedelta(days=2)
    time = start_time
    c = Competition()
    c.discipline = Discipline.query.filter(Discipline.name == disc).first()
    c.dancing_class = DancingClass.query.filter(DancingClass.name == d_class).first()
    c.mode = CompetitionMode.single_partner
    if disc == SLOW_WALTZ or disc == SAMBA or disc == SALSA:
        time = time + timedelta(hours=1)
    if disc == TANGO or disc == CHA_CHA_CHA or disc == BACHATA:
        time = time + timedelta(hours=2)
    if disc == VIENNESE_WALTZ or disc == RUMBA or disc == MERENGUE:
        time = time + timedelta(hours=3)
    if disc == SLOW_FOXTROT or disc == PASO_DOBLE or disc == POLKA:
        time = time + timedelta(hours=4)
    if disc == QUICKSTEP or disc == JIVE:
        time = time + timedelta(hours=5)
    if d_class == TEST:
        time = time + timedelta(hours=-1)
    if d_class == BREITENSPORT_QUALIFICATION:
        time = time + timedelta(minutes=0)
    if d_class == BREITENSPORT_QUALIFICATION:
        time = time + timedelta(minutes=0)
    if d_class == AMATEURS:
        time = time + timedelta(minutes=10)
    if d_class == CHAMPIONS:
        time = time + timedelta(minutes=20)
    if d_class == OPEN_CLASS:
        time = time + timedelta(hours=6)
    c.floors = 1
    c.when = time
    c.event = g.event
    if d_class in BREITENSPORT_COMPETITIONS:
        c.qualification = Competition.query.join(DancingClass, Discipline)\
            .filter(DancingClass.name == BREITENSPORT_QUALIFICATION, Discipline.name == disc).first()
    db.session.commit()


@bp.route('/dances', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def dances():
    dance_form = DanceForm()
    if dance_form.dance_submit.name in request.form:
        if dance_form.validate_on_submit():
            check = Dance.query.filter(or_(Dance.name == dance_form.name.data, Dance.tag == dance_form.tag.data))\
                .first()
            if check is None:
                d = Dance()
                d.name = dance_form.name.data
                d.tag = dance_form.tag.data
                db.session.add(d)
                db.session.commit()
                flash("Created {} as a dance.".format(d.name))
                return redirect(url_for('adjudication_system.dances'))
            else:
                flash("Cannot create {} dance, a dance with that name or tag already exists."
                      .format(dance_form.name.data), "alert-warning")
                return redirect(url_for('adjudication_system.dances'))
    all_dances = Dance.query.order_by(Dance.discipline_id, Dance.name).all()
    return render_template('adjudication_system/dances.html', dance_form=dance_form, all_dances=all_dances)


@bp.route('/edit_dance/<int:dance_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def edit_dance(dance_id):
    dance = Dance.query.filter(Dance.dance_id == dance_id).first()
    if dance is not None:
        dance_form = DanceForm()
        if request.method == "GET":
            dance_form.name.data = dance.name
            dance_form.tag.data = dance.tag
        if 'save_changes' in request.form:
            if dance_form.validate_on_submit():
                check = Dance.query.filter(or_(Dance.name == dance_form.name.data, Dance.tag == dance_form.tag.data))\
                    .first()
                if check is None or check.dance_id == dance.dance_id:
                    dance.name = dance_form.name.data
                    dance.tag = dance_form.tag.data
                    db.session.commit()
                    flash("Edited {}.".format(dance))
                    return redirect(url_for('adjudication_system.dances'))
                else:
                    flash("Cannot change {} dance, a dance with that name or tag already exists."
                          .format(dance_form.name.data), "alert-warning")
                    return redirect(url_for('adjudication_system.edit_dance'))
        if 'delete_dance' in request.form:
            if dance.deletable():
                db.session.delete(dance)
                db.session.commit()
                flash("Deleted {}.".format(dance))
                return redirect(url_for('adjudication_system.dances'))
            else:
                flash("Cannot delete {}, it has disciplines associated with it.".format(dance))
                return redirect(url_for('adjudication_system.edit_dance'))
    else:
        flash("Invalid id.")
        return redirect(url_for('adjudication_system.dances'))
    return render_template('adjudication_system/edit_dance.html', dance_form=dance_form, dance=dance)


@bp.route('/disciplines', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def disciplines():
    discipline_form = DisciplineForm()
    if discipline_form.discipline_submit.name in request.form:
        if discipline_form.validate_on_submit():
            check = Discipline.query.filter(Discipline.name == discipline_form.name.data).first()
            if check is None:
                d = Discipline()
                d.name = discipline_form.name.data
                d.dances = Dance.query.filter(Dance.dance_id.in_(discipline_form.dances.data)).all()
                db.session.add(d)
                db.session.commit()
                flash("Created {} as a discipline.".format(d))
                return redirect(url_for('adjudication_system.disciplines'))
            else:
                flash("Cannot create {} discipline, it already exists.".format(discipline_form.name.data),
                      "alert-warning")
                return redirect(url_for('adjudication_system.disciplines'))
    all_disciplines = Discipline.query.all()
    return render_template('adjudication_system/disciplines.html', discipline_form=discipline_form,
                           all_disciplines=all_disciplines)


@bp.route('/edit_discipline/<int:discipline_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def edit_discipline(discipline_id):
    discipline = Discipline.query.filter(Discipline.discipline_id == discipline_id).first()
    if discipline is not None:
        discipline_form = DisciplineForm(discipline)
        if 'save_changes' in request.form:
            if discipline_form.validate_on_submit():
                check = Discipline.query.filter(Discipline.name == discipline_form.name.data).first()
                if check is None or check.discipline_id == discipline.discipline_id:
                    discipline.name = discipline_form.name.data
                    discipline.dances = Dance.query.filter(Dance.dance_id.in_(discipline_form.dances.data)).all()
                    db.session.commit()
                    flash("Edited {}.".format(discipline))
                    return redirect(url_for('adjudication_system.disciplines'))
                else:
                    flash("Cannot change name to {}. A discipline with that name already exists."
                          .format(discipline_form.name.data), "alert-warning")
                    return redirect(url_for('adjudication_system.edit_discipline'))
        if 'delete_discipline' in request.form:
            if discipline.deletable():
                db.session.delete(discipline)
                db.session.commit()
                flash("Deleted {}.".format(discipline))
                return redirect(url_for('adjudication_system.disciplines'))
            else:
                flash("Cannot delete {}, it has competitions associated with it.".format(discipline))
                return redirect(url_for('adjudication_system.edit_discipline'))
    else:
        flash("Invalid id.")
        return redirect(url_for('adjudication_system.disciplines'))
    return render_template('adjudication_system/edit_discipline.html', discipline_form=discipline_form,
                           discipline=discipline)


@bp.route('/dancing_classes', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def dancing_classes():
    dancing_class_form = DancingClassForm()
    if dancing_class_form.dancing_class_submit.name in request.form:
        if dancing_class_form.validate_on_submit():
            check = DancingClass.query.filter(DancingClass.name == dancing_class_form.name.data).first()
            if check is None:
                d = DancingClass()
                d.name = dancing_class_form.name.data
                db.session.add(d)
                db.session.commit()
                flash("Created {} as a class.".format(d))
                return redirect(url_for('adjudication_system.dancing_classes'))
            else:
                flash("Cannot create {} class, it already exists.".format(dancing_class_form.name.data),
                      "alert-warning")
                return redirect(url_for('adjudication_system.dancing_classes'))
    all_classes = DancingClass.query.all()
    return render_template('adjudication_system/dancing_classes.html', dancing_class_form=dancing_class_form,
                           all_classes=all_classes)


@bp.route('/edit_dancing_class/<int:dancing_class_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def edit_dancing_class(dancing_class_id):
    dancing_class = DancingClass.query.filter(DancingClass.dancing_class_id == dancing_class_id).first()
    if dancing_class is not None:
        dancing_class_form = DancingClassForm()
        if request.method == "GET":
            dancing_class_form.name.data = dancing_class.name
        if 'save_changes' in request.form:
            if dancing_class_form.validate_on_submit():
                check = DancingClass.query.filter(DancingClass.name == dancing_class_form.name.data).first()
                if check is None or check.dancing_class_id == dancing_class.dancing_class_id:
                    dancing_class.name = dancing_class_form.name.data
                    db.session.commit()
                    flash("Edited {}.".format(dancing_class))
                    return redirect(url_for('adjudication_system.dancing_classes'))
                else:
                    flash("Cannot change name to {}. A class with that name already exists."
                          .format(dancing_class_form.name.data), "alert-warning")
                    return redirect(url_for('adjudication_system.edit_dancing_class'))
        if 'delete_class' in request.form:
            if dancing_class.deletable():
                db.session.delete(dancing_class)
                db.session.commit()
                flash("Deleted {}.".format(dancing_class))
                return redirect(url_for('adjudication_system.dancing_classes'))
            else:
                flash("Cannot delete {}, it has competitions associated with it.".format(dancing_class))
                return redirect(url_for('adjudication_system.edit_dancing_class'))
    else:
        flash("Invalid id.")
        return redirect(url_for('adjudication_system.dancing_classes'))
    return render_template('adjudication_system/edit_dancing_class.html', dancing_class_form=dancing_class_form,
                           dancing_class=dancing_class)


@bp.route('/available_adjudicators', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def available_adjudicators():
    all_adjudicators = Adjudicator.query.order_by(Adjudicator.name).all()
    form = CreateAdjudicatorForm()
    if request.method == POST:
        if form.adjudicator_contestant_submit.name in request.form:
            if form.validate_on_submit():
                check_adjudicator = Adjudicator.query.filter(Adjudicator.name == form.name.data).first()
                if check_adjudicator is None:
                    u = User()
                    u.username = form.tag.data
                    u.set_password(form.tag.data)
                    u.is_active = True
                    u.access = ACCESS[ADJUDICATOR]
                    adj = Adjudicator()
                    adj.name = form.name.data
                    adj.tag = generate_tag("{}".format(form.tag.data).upper())
                    adj.user = u
                    db.session.add(adj)
                    db.session.commit()
                    flash("Added {name} as an adjudicator, with tag, username and password as {tag}."
                          .format(name=form.name.data, tag=adj.tag), "alert-success")
                else:
                    flash("{} is already an adjudicator in the system.".format(form.name.data))
                return redirect(url_for("adjudication_system.available_adjudicators"))
    return render_template('adjudication_system/available_adjudicators.html', all_adjudicators=all_adjudicators,
                           form=form)


def generate_tag(tag):
    original_tag = tag
    tags = [a.tag for a in Adjudicator.query.all()]
    for i in range(1, len(tags) + 1):
        if tag not in tags:
            break
        else:
            tag = "{tag}{num}".format(tag=original_tag, num=i)
    return tag


@bp.route('/delete_adjudicator/<int:adjudicator_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def delete_adjudicator(adjudicator_id):
    adjudicator = Adjudicator.query.filter(Adjudicator.adjudicator_id == adjudicator_id).first()
    if adjudicator is not None:
        flash("Deleted {} from the system.".format(adjudicator))
        db.session.delete(adjudicator.user)
        db.session.commit()
    else:
        flash("Invalid id.", "alert-warning")
    return redirect(url_for("adjudication_system.available_adjudicators"))


@bp.route('/adjudicator_assignments', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def adjudicator_assignments():
    if g.event is not None:
        all_adjudicators = Adjudicator.query.all()
        if request.method == "POST":
            form = request.form
            if 'save_assignments' in form:
                for comp in g.event.competitions:
                    if comp.is_configurable():
                        checks = [a for a in ["{comp_id}-{adj_id}".format(comp_id=comp.competition_id,
                                                                          adj_id=adj.adjudicator_id)
                                              for adj in all_adjudicators] if a in form]
                        adjudicators = [int(a) for a in [a.split('-')[1] for a in checks]]
                        comp.adjudicators = Adjudicator.query.filter(Adjudicator.adjudicator_id.in_(adjudicators)).all()
                db.session.commit()
                flash("Saved assignments", "alert-success")
    else:
        flash("There is no event yet for adjudicators to be assigned to.")
        return redirect(url_for("main.dashboard"))
    return render_template('adjudication_system/adjudicator_assignments.html', all_adjudicators=all_adjudicators)


@bp.route('/available_dancers', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def available_dancers():
    form = DancerForm()
    import_form = ImportDancersForm()
    if request.method == POST:
        if form.submit.name in request.form:
            if form.validate_on_submit():
                check_dancer = Dancer.query.filter(Dancer.number == form.number.data,
                                                   Dancer.role == form.role.data).first()
                if check_dancer is None:
                    dancer = Dancer()
                    dancer.name = form.name.data
                    dancer.number = form.number.data
                    dancer.role = form.role.data
                    dancer.team = form.team.data
                    db.session.add(dancer)
                    db.session.commit()
                    flash("Created {name} ({number}) as a {role}"
                          .format(name=dancer.name, number=dancer.number, role=dancer.role), "alert-success")
                else:
                    flash("{name} ({number}) as a {role} is already in the system."
                          .format(name=check_dancer.name, number=check_dancer.number, role=check_dancer.role))
                return redirect(url_for("adjudication_system.available_dancers"))
        if import_form.import_submit.name in request.form:
            if import_form.validate_on_submit():
                import_list = import_form.import_string.data.split('\r\n')
                counter = 0
                for import_string in import_list:
                    d = import_string.split(',')
                    if len(d) == 5:
                        if d[3] == 'TRUE':
                            check_dancer = Dancer.query.filter(Dancer.number == d[0], Dancer.role == LEAD).first()
                            if check_dancer is None:
                                dancer = Dancer()
                                dancer.number = d[0]
                                dancer.name = d[1]
                                dancer.team = d[2]
                                dancer.role = LEAD
                                db.session.add(dancer)
                                counter += 1
                        if d[4] == 'TRUE':
                            check_dancer = Dancer.query.filter(Dancer.number == d[0], Dancer.role == FOLLOW).first()
                            if check_dancer is None:
                                dancer = Dancer()
                                dancer.number = d[0]
                                dancer.name = d[1]
                                dancer.team = d[2]
                                dancer.role = FOLLOW
                                db.session.add(dancer)
                                counter += 1
                db.session.commit()
                if counter > 0:
                    flash("Imported {} unique dancers.".format(counter), "alert-success")
                else:
                    flash("No new dancers imported.")
                return redirect(url_for("adjudication_system.available_dancers"))
    dancers = Dancer.query.all()
    return render_template('adjudication_system/available_dancers.html', form=form, dancers=dancers,
                           import_form=import_form)


@bp.route('/edit_dancer/<int:dancer_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def edit_dancer(dancer_id):
    dancer = Dancer.query.filter(Dancer.dancer_id == dancer_id).first()
    if dancer is not None:
        form = EditDancerForm(dancer)
        if 'save_changes' in request.form:
            if form.validate_on_submit():
                comps = Competition.query.filter(Competition.competition_id.in_(form.competitions.data)).all()
                dancer.set_competitions(comps)
                db.session.commit()
                flash("Edited {dancer} ({role}).".format(dancer=dancer, role=dancer.role))
                return redirect(url_for('adjudication_system.available_dancers'))
        if 'delete_dancer' in request.form:
            if dancer.deletable():
                flash("Deleted {dancer} ({role}).".format(dancer=dancer, role=dancer.role))
                db.session.delete(dancer)
                db.session.commit()
            else:
                flash("Cannot delete {dancer} ({role}).".format(dancer=dancer, role=dancer.role))
            return redirect(url_for('adjudication_system.available_dancers'))
    else:
        flash("Invalid id.")
        return redirect(url_for('adjudication_system.available_dancers'))
    return render_template('adjudication_system/edit_dancer.html', form=form, dancer=dancer)


@bp.route('/available_couples', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def available_couples():
    form = CoupleForm()
    import_form = ImportCouplesForm()
    if request.method == POST:
        if form.submit.name in request.form:
            if form.validate_on_submit():
                check_couple = Couple.query.filter(Couple.lead == form.lead.data, Couple.follow == form.follow.data) \
                    .first()
                if check_couple is None:
                    couple = Couple()
                    couple.lead = form.lead.data
                    couple.follow = form.follow.data
                    couple.number = form.lead.data.number
                    couple.competitions = Competition.query\
                        .filter(Competition.competition_id.in_(form.competitions.data)).all()
                    db.session.add(couple)
                    db.session.commit()
                    flash("Created couple with {lead} as lead and {follow} as follow in the competitions: {comps}."
                          .format(lead=form.lead.data, follow=form.follow.data,
                                  comps=', '.join([c.__repr__() for c in couple.competitions])), "alert-success")
                else:
                    flash("{lead} and {follow} are already a couple."
                          .format(lead=form.lead.data, follow=form.follow.data))
                return redirect(url_for("adjudication_system.available_couples"))
        if import_form.import_submit.name in request.form:
            if import_form.validate_on_submit():
                import_list = import_form.import_string.data.split('\r\n')
                counter = 0
                for import_string in import_list:
                    d = import_string.split(',')
                    if len(d) == 4:
                        check_lead = Dancer.query.filter(Dancer.name == d[0], Dancer.role == LEAD).first()
                        check_follow = Dancer.query.filter(Dancer.name == d[1], Dancer.role == FOLLOW).first()
                        check_competition = Competition.query.join(Discipline, DancingClass)\
                            .filter(Discipline.name == d[2], DancingClass.name == d[3]).first()
                        if check_lead is not None and check_follow is not None and check_competition is not None:
                            couple = Couple.query.filter(Couple.lead == check_lead, Couple.follow == check_follow)\
                                .first()
                            if couple is None:
                                couple = Couple()
                                couple.lead = check_lead
                                couple.follow = check_follow
                                couple.number = check_lead.number
                            counter += 1
                            couple.competitions.append(check_competition)
                            db.session.add(couple)
                db.session.commit()
                if counter > 0:
                    flash("Imported/Updated {} couples."
                          .format(counter), "alert-success")
                else:
                    flash("No new couples imported.")
                return redirect(url_for("adjudication_system.available_couples"))
    couples = Couple.query.all()
    return render_template('adjudication_system/available_couples.html', form=form, import_form=import_form,
                           couples=couples)


@bp.route('/edit_couple/<int:couple_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def edit_couple(couple_id):
    couple = Couple.query.filter(Couple.couple_id == couple_id).first()
    if couple is not None:
        form = EditCoupleForm(couple)
        if 'save_changes' in request.form:
            if form.validate_on_submit():
                couple.competitions = Competition.query\
                    .filter(Competition.competition_id.in_(form.competitions.data)).all()
                db.session.commit()
                flash("Couple data {lead}, {follow} updated.".format(lead=couple.lead, follow=couple.follow))
                return redirect(url_for('adjudication_system.available_couples'))
    else:
        flash("Invalid id.")
        return redirect(url_for('adjudication_system.available_couples'))
    return render_template('adjudication_system/edit_couple.html', form=form, couple=couple)


@bp.route('/delete_couple/<int:couple_id>', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def delete_couple(couple_id):
    couple = Couple.query.filter(Couple.couple_id == couple_id).first()
    if couple is not None:
        if couple.deletable():
            flash("Deleted {lead} and {follow} as a couple from the system."
                  .format(lead=couple.lead, follow=couple.follow))
            db.session.delete(couple)
            db.session.commit()
        else:
            flash("Cannot delete couple.")
    else:
        flash("Invalid id.", "alert-warning")
    return redirect(url_for("adjudication_system.available_couples"))


@bp.route('/competition', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def competition():
    competition_id = request.args.get('competition_id', type=int)
    comp = Competition.query.filter(Competition.competition_id == competition_id).first()
    if comp is None:
        return redirect(url_for("adjudication_system.event"))
    if len(comp.rounds) > 0 and comp.has_adjudicators():
        if not (len(comp.rounds) == 1 and len(comp.rounds[0].heats) == 0):
            return redirect(url_for("adjudication_system.progress", round_id=comp.last_round().round_id))
    competition_form = CompetitionForm(comp)
    round_form = CreateFirstRoundForm(comp)
    if competition_form.comp_submit.name in request.form:
        if competition_form.validate_on_submit():
            comp.dancing_class = competition_form.dancing_class.data
            comp.discipline = competition_form.discipline.data
            comp.floors = competition_form.floors.data
            comp.when = competition_form.when.data
            comp.qualification = competition_form.qualification.data
            comp.mode = competition_form.mode.data
            comp.adjudicators = Adjudicator.query \
                .filter(Adjudicator.adjudicator_id.in_(competition_form.adjudicators.data)).all()
            comp.couples = Couple.query.filter(Couple.couple_id.in_(competition_form.competition_couples.data)).all()
            comp.leads = Dancer.query.filter(Dancer.dancer_id.in_(competition_form.competition_leads.data)).all()
            comp.follows = Dancer.query.filter(Dancer.dancer_id.in_(competition_form.competition_follows.data)).all()
            db.session.commit()
            flash("Changes to {} saved.".format(comp), "alert-success")
            return redirect(url_for("adjudication_system.competition", competition_id=comp.competition_id))
    if round_form.round_submit.name in request.form:
        if round_form.validate_on_submit():
            r = Round()
            r.type = round_form.type.data
            r.min_marks = round_form.min_marks.data
            r.max_marks = max(round_form.min_marks.data, round_form.max_marks.data)
            r.is_active = False
            r.competition = comp
            r.dances = Dance.query.filter(Dance.dance_id.in_(round_form.dances.data)).all()
            for dance in r.dances:
                da = DanceActive()
                da.round = r
                da.dance = dance
                r.dance_active.append(da)
            r.couples = comp.generate_couples()
            if round_form.type.data == RoundType.final.name:
                r.create_final()
            else:
                r.create_heats(round_form.heats.data)
            db.session.commit()
            flash("Created {type} for {comp}.".format(type=r.type.value, comp=comp), "alert-success")
            return redirect(url_for("adjudication_system.progress", round_id=r.round_id))
    return render_template('adjudication_system/competition.html', competition=comp, competition_form=competition_form,
                           round_form=round_form)


@bp.route('/progress', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def progress():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    if not dancing_round.has_adjudicators():
        flash("Please assign adjudicators first.", "alert-warning")
        return redirect(url_for("adjudication_system.competition",
                                competition_id=dancing_round.competition.competition_id))
    if dancing_round.first_round_after_qualification_split():
        round_form = CreateFirstRoundForm(dancing_round.competition)
    else:
        round_form = ConfigureNextRoundForm(dancing_round)
    if request.method == 'POST':
        if "split" in request.form:
            return redirect(url_for("adjudication_system.split", round_id=dancing_round.round_id))
        if "configure" in request.form:
            if round_form.validate_on_submit():
                if dancing_round.first_round_after_qualification_split():
                    couples = [c for c in dancing_round.couples if str(c.couple_id) in request.form]
                    dancing_round.type = round_form.type.data
                    dancing_round.min_marks = round_form.min_marks.data
                    dancing_round.max_marks = max(round_form.min_marks.data, round_form.max_marks.data)
                    dancing_round.is_active = False
                    dancing_round.dances = Dance.query.filter(Dance.dance_id.in_(round_form.dances.data)).all()
                    for dance in dancing_round.dances:
                        da = DanceActive()
                        da.round = dancing_round
                        da.dance = dance
                        dancing_round.dance_active.append(da)
                    dancing_round.couples = couples
                    dancing_round.create_heats(round_form.heats.data)
                    db.session.commit()
                    flash("Configured {type} for {comp}."
                          .format(type=dancing_round.type.value, comp=dancing_round.competition), "alert-success")
                    return redirect(url_for("adjudication_system.progress", round_id=dancing_round.round_id))
                if dancing_round.competition.is_change_per_dance():
                    dancers = dancing_round.change_per_dance_dancers_rows()
                    if round_form.type.data != RoundType.re_dance.name:
                        dancers = [d for d in dancers if d['crosses'] >= round_form.cutoff.data or d['crosses'] == -1]
                    else:
                        dancers = [d for d in dancers if d['crosses'] < round_form.cutoff.data]
                    dancers = [d['dancer'] for d in dancers if str(d['dancer'].dancer_id) in request.form]
                    leads = [d for d in dancers if d.role == LEAD]
                    follows = [d for d in dancers if d.role == FOLLOW]
                    if len(leads) == len(follows):
                        couples = create_couples_list(leads=leads, follows=follows)
                    else:
                        flash("Cannot configure the next round with {leads} leads and {follows} follows. Please check "
                              "the list again.".format(leads=len(leads), follows=len(follows)), "alert-warning")
                        return render_template('adjudication_system/progress.html', dancing_round=dancing_round,
                                               round_form=round_form)
                else:
                    if dancing_round.is_final():
                        couples = [c for c in dancing_round.couples if str(c.couple_id) in request.form]
                    else:
                        couples = [r for r in dancing_round.round_results if str(r.couple.couple_id) in request.form]
                        if round_form.type.data != RoundType.re_dance.name:
                            couples = [r.couple for r in couples if r.marks >= round_form.cutoff.data or r.marks == -1]
                        else:
                            couples = [r.couple for r in couples if r.marks < round_form.cutoff.data]
                r = Round()
                r.type = round_form.type.data
                r.min_marks = round_form.min_marks.data
                r.max_marks = max(round_form.min_marks.data, round_form.max_marks.data)
                r.is_active = False
                r.competition = dancing_round.competition
                r.dances = Dance.query.filter(Dance.dance_id.in_(round_form.dances.data)).all()
                for dance in r.dances:
                    da = DanceActive()
                    da.round = r
                    da.dance = dance
                    r.dance_active.append(da)
                if dancing_round.competition.mode == CompetitionMode.change_per_round:
                    round_couples = create_couples_list(couples=couples)
                else:
                    round_couples = couples
                r.couples = round_couples
                if round_form.type.data == RoundType.final.name:
                    r.create_final()
                else:
                    r.create_heats(round_form.heats.data)
                db.session.commit()
                flash("Created {type} for {competition}."
                      .format(type=r.type.value, competition=dancing_round.competition), "alert-success")
                return redirect(url_for("adjudication_system.progress", round_id=r.round_id))
        if "delete" in request.form:
            comp = dancing_round.competition
            flash("Deleted {}.".format(dancing_round))
            db.session.delete(dancing_round)
            db.session.commit()
            try:
                return redirect(url_for("adjudication_system.progress", round_id=comp.last_round().round_id))
            except AttributeError:
                return redirect(url_for("adjudication_system.competition", competition_id=comp.competition_id))
    return render_template('adjudication_system/progress.html', dancing_round=dancing_round, round_form=round_form)


def split_breitensport(dancing_round, chosen_split):
    competitions = [c for c in dancing_round.competition.qualifications]
    competitions.sort(key=lambda comp: comp.when)
    for idx, dc in enumerate(chosen_split):
        competitions[idx].couples.extend(chosen_split[idx])
        db.session.commit()


# noinspection PyTypeChecker
def split_couples_into_competitions(dancing_round):
    num_comps = len(dancing_round.competition.qualifications)
    round_result_list = [r.marks for r in dancing_round.round_results]
    unique_results = list(set(round_result_list))
    unique_results.sort()
    combs = []
    for c in combinations(range(1, len(unique_results)), num_comps - 1):
        combs.append(split_list(unique_results, list(c)))
    splittings = [[[] for _ in range(num_comps)] for _ in combs]
    for i in range(len(combs)):
        for j in range(num_comps):
            for r in dancing_round.round_results:
                if r.marks in combs[i][j]:
                    splittings[i][j].append(r.couple)
    splittings.sort(key=lambda x: statistics.stdev([len(s) for s in x]))
    splitting_strings = [' / '.join([str(st) for st in s]) for s in [[len(l) for l in sp] for sp in splittings]]
    splitting_results = {}
    for i in range(len(combs)):
        splitting_results.update({splitting_strings[i]: splittings[i]})
    return splitting_results


def split_list(l, indices):
    container = [l[:indices[0]]]
    for idx in range(len(indices)-1):
        container.append(l[indices[idx]:indices[idx+1]])
    container.append(l[indices[-1]:])
    return container


@bp.route('/split', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def split():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    if dancing_round.is_split():
        return redirect(url_for("adjudication_system.progress", round_id=dancing_round.round_id))
    if len(dancing_round.competition.qualifications) == 1:
        flash("There is only one competition to qualify for. Cannot split couples. Please add a second qualification.")
        return redirect(url_for("adjudication_system.progress", round_id=dancing_round.round_id))
    form = SplitForm(split_couples_into_competitions(dancing_round))
    if form.validate_on_submit():
        split_breitensport(dancing_round, split_couples_into_competitions(dancing_round)[form.scenarios.data])
        flash("{} split!".format(dancing_round), "alert-success")
        return redirect(url_for("adjudication_system.progress", round_id=dancing_round.round_id))
    return render_template('adjudication_system/split.html', dancing_round=dancing_round, form=form)


@bp.route('/reports', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def reports():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    if dancing_round.first_dance() is None:
        flash('Please configure the dancing round first.', "alert-warning")
        return redirect(url_for('adjudication_system.progress', round_id=dancing_round.round_id))
    form = PrintReportsForm()
    return render_template('adjudication_system/reports.html', dancing_round=dancing_round, form=form)


@bp.route('/reports_print', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def reports_print():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    form = PrintReportsForm()
    return render_template('adjudication_system/reports_print.html', dancing_round=dancing_round, form=form)


@bp.route('/floor_management', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def floor_management():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    dance_id = request.args.get('dance_id', 0, type=int)
    if dance_id == 0:
        if dancing_round.has_dances():
            return redirect(url_for('adjudication_system.floor_management', round_id=dancing_round.round_id,
                                    dance_id=dancing_round.first_dance().dance_id))
        else:
            flash('Please configure the dancing round first.', "alert-warning")
            return redirect(url_for('adjudication_system.progress', round_id=dancing_round.round_id))
    elif not dancing_round.has_dance(dance_id):
        return redirect(url_for('adjudication_system.floor_management', round_id=dancing_round.round_id,
                                dance_id=dancing_round.first_dance().dance_id))
    dance = Dance.query.get(dance_id)
    if request.method == 'POST':
        if "save" in request.form:
            for present_id in request.form:
                try:
                    cp = CouplePresent.query.get(present_id)
                    cp.present = True
                except AttributeError:
                    pass
        elif "refresh" in request.form:
            pass
        else:
            presents = [heat.couples_present for heat in dancing_round.heats
                        if heat.dance_id == int([f for f in request.form][0])]
            for l in presents:
                for cp in l:
                    cp.present = False
        db.session.commit()
    return render_template('adjudication_system/floor_management.html', dancing_round=dancing_round, dance=dance)


@bp.route('/adjudication', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def adjudication():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    dance_id = request.args.get('dance_id', 0, type=int)
    if dance_id == 0:
        if dancing_round.has_dances():
            return redirect(url_for('adjudication_system.adjudication', round_id=dancing_round.round_id,
                                    dance_id=dancing_round.first_dance().dance_id))
        else:
            flash('Please configure the dancing round first.', "alert-warning")
            return redirect(url_for('adjudication_system.progress', round_id=dancing_round.round_id))
    elif not dancing_round.has_dance(dance_id):
        return redirect(url_for('adjudication_system.adjudication', round_id=dancing_round.round_id,
                                dance_id=dancing_round.first_dance().dance_id))
    dance = Dance.query.get(dance_id)
    if request.method == 'POST':
        if "evaluate" in request.form:
            dancing_round.deactivate()
            if not dancing_round.is_final():
                if dancing_round.can_evaluate():
                    couple_marks = {}
                    couples = dancing_round.couples
                    for couple in couples:
                        marks = [heat.marks for heat in dancing_round.heats]
                        count = 0
                        for mark in marks:
                            for m in mark:
                                if m.mark and m.couple == couple:
                                    count += 1
                        couple_marks.update({couple: count})
                    previous_round = dancing_round.previous_round()
                    direct_qualified_couples = []
                    if dancing_round.type == RoundType.re_dance:
                        max_mark = max(couple_marks.values()) + 1
                        if dancing_round.competition.is_change_per_dance():
                            direct_qualified_couples = [c for c in previous_round.couples if c.number
                                                        not in [c.number for c in couples]]
                        else:
                            direct_qualified_couples = [c for c in previous_round.couples if c.number
                                                        not in [c.number for c in couples]]
                        for couple in direct_qualified_couples:
                            couple_marks.update({couple: max_mark})
                    for couple in couples + direct_qualified_couples:
                        result = RoundResult()
                        result.couple = couple
                        result.marks = couple_marks[couple]
                        result.round = dancing_round
                    round_result_list = [r.marks for r in dancing_round.round_results]
                    result_map = generate_placings(round_result_list)
                    for result in dancing_round.round_results:
                        result.placing = result_map[result.marks]
                    if dancing_round.type == RoundType.re_dance:
                        for result in dancing_round.round_results:
                            if result.couple in direct_qualified_couples:
                                result.marks = -1
                    db.session.commit()
                    return redirect(url_for("adjudication_system.progress",
                                            round_id=request.args.get('round_id', type=int)))
                else:
                    flash(Markup("Cannot evaluate round.<br/><br/>{}"
                                 .format('<br/>'.join(dancing_round.evaluation_errors()))), "alert-danger")
            else:
                if dancing_round.is_completed():
                    flash('Final evaluated.', 'alert-success')
                else:
                    flash('Cannot evaluate the final. Please check the placings.')
        if 'save_marks' in request.form:
            if not dancing_round.is_dance_active(dance):
                for mark in dancing_round.marks(dance):
                    mark.mark = str(mark.mark_id) in request.form
                db.session.commit()
                flash('Placings for {dancing_round} - {dance} saved.'.format(dancing_round=dancing_round, dance=dance))
            else:
                flash('Cannot change marks when a dance is being adjudicated.', 'alert-warning')
            return redirect(url_for("adjudication_system.adjudication", round_id=request.args.get('round_id', type=int),
                                    dance_id=dance.dance_id))
        if 'save_final_placings' in request.form:
            if not dancing_round.is_dance_active(dance):
                for placing in [p for p in dancing_round.final_placings if p.dance == dance]:
                    try:
                        placing.final_placing = int(request.form[str(placing.final_placing_id)])
                    except ValueError:
                        placing.final_placing = 0
                db.session.commit()
                flash('Placings for {dancing_round} - {dance} saved.'.format(dancing_round=dancing_round, dance=dance))
            else:
                flash('Cannot change marks when a dance is being adjudicated.', 'alert-warning')
            return redirect(url_for("adjudication_system.adjudication", round_id=request.args.get('round_id', type=int),
                                    dance_id=dance.dance_id))
    return render_template('adjudication_system/adjudication.html', dancing_round=dancing_round, dance=dance)


@bp.route('/final_result', methods=['GET'])
@login_required
@requires_access_level([ACCESS[TOURNAMENT_OFFICE_MANAGER]])
def final_result():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.event"))
    skating = dancing_round.skating_summary()
    return render_template('adjudication_system/final_result.html', dancing_round=dancing_round, skating=skating)


@bp.route('/adjudicator_dashboard', methods=['GET'])
@login_required
@requires_access_level([ACCESS[ADJUDICATOR]])
def adjudicator_dashboard():
    current_user.adjudicator.round = 0
    current_user.adjudicator.dance = 0
    db.session.commit()
    return render_template('adjudication_system/adjudicator_dashboard.html')


@bp.route('/adjudicate_start_page', methods=['GET'])
@login_required
@requires_access_level([ACCESS[ADJUDICATOR]])
def adjudicate_start_page():
    current_user.adjudicator.round = 0
    current_user.adjudicator.dance = 0
    db.session.commit()
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("main.dashboard"))
    if not dancing_round.is_active:
        flash("{} is currently closed.".format(dancing_round.competition))
        return redirect(url_for("main.dashboard"))
    return render_template('adjudication_system/adjudicate_start_page.html', dancing_round=dancing_round)


@bp.route('/adjudicate', methods=['GET'])
@login_required
@requires_access_level([ACCESS[ADJUDICATOR]])
def adjudicate():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("main.dashboard"))
    if not dancing_round.is_active:
        flash("{} is currently closed.".format(dancing_round.competition))
        return redirect(url_for("main.dashboard"))
    dance_id = request.args.get('dance_id', 0, type=int)
    if dance_id == 0:
        return redirect(url_for('adjudication_system.adjudicate', round_id=dancing_round.round_id,
                                dance_id=dancing_round.first_dance().dance_id))
    dance = Dance.query.get(dance_id)
    current_user.adjudicator.round = dancing_round_id
    current_user.adjudicator.dance = dance_id
    db.session.commit()
    return render_template('adjudication_system/adjudicate.html', dancing_round=dancing_round, dance=dance)


@bp.route('/floor_manager_start_page', methods=['GET'])
@login_required
@requires_access_level([ACCESS[FLOOR_MANAGER]])
def floor_manager_start_page():
    return render_template('adjudication_system/floor_manager_start_page.html')


@bp.route('/floor_manager', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[FLOOR_MANAGER]])
def floor_manager():
    dancing_round_id = request.args.get('round_id', 0, type=int)
    dancing_round = Round.query.filter(Round.round_id == dancing_round_id).first()
    if dancing_round is None:
        return redirect(url_for("adjudication_system.floor_manager_start_page"))
    dance_id = request.args.get('dance_id', 0, type=int)
    if dance_id == 0:
        if dancing_round.has_dances():
            return redirect(url_for('adjudication_system.floor_manager', round_id=dancing_round.round_id,
                                    dance_id=dancing_round.first_dance().dance_id))
        else:
            return redirect(url_for('adjudication_system.floor_manager_start_page', round_id=dancing_round.round_id))
    elif not dancing_round.has_dance(dance_id):
        return redirect(url_for('adjudication_system.floor_manager', round_id=dancing_round.round_id,
                                dance_id=dancing_round.first_dance().dance_id))
    dance = Dance.query.get(dance_id)
    return render_template('adjudication_system/floor_manager.html', dancing_round=dancing_round, dance=dance)


@bp.route('/starting_lists', methods=['GET'])
def starting_lists():
    competitions = Competition.query.all()
    competitions = [c for c in competitions if len(c.couples) > 0 and c.dancing_class.name != TEST]
    competition_id = request.args.get('competition', 0, int)
    if competition_id in [c.competition_id for c in competitions]:
        comp = Competition.query.get(competition_id)
        return render_template('adjudication_system/competition_starting_lists.html', comp=comp)
    else:
        if competition_id > 0:
            flash('Competition not found.')
        return render_template('adjudication_system/starting_lists.html', competitions=competitions)


@bp.route('/heat_lists', methods=['GET'])
def heat_lists():
    competitions = Competition.query.all()
    competitions = [c for c in competitions if len(c.rounds) > 0 and c.dancing_class.name != TEST]
    competition_id = request.args.get('competition', 0, int)
    if competition_id in [c.competition_id for c in competitions]:
        comp = Competition.query.get(competition_id)
        return render_template('adjudication_system/competition_heat_lists.html', comp=comp)
    else:
        if competition_id > 0:
            flash('Competition not found.')
        return render_template('adjudication_system/heat_lists.html', competitions=competitions)


@bp.route('/starting_numbers', methods=['GET'])
def starting_numbers():
    all_dancers = Dancer.query.all()
    all_numbers = []
    dancers = []
    for d in all_dancers:
        if d.number not in all_numbers:
            all_numbers.append(d.number)
            dancers.append(d)
    return render_template('adjudication_system/competition_starting_numbers.html', dancers=dancers)


@bp.route('/results', methods=['GET'])
def results():
    competitions = Competition.query.order_by(Competition.when).all()
    competitions = [c for c in competitions if c.results_published and len(c.qualifications) == 0
                    and c.dancing_class.name != TEST]
    competition_id = request.args.get('competition', 0, int)
    if competition_id in [c.competition_id for c in competitions]:
        comp = Competition.query.get(competition_id)
        return render_template('adjudication_system/competition_results.html', comp=comp)
    else:
        if competition_id > 0:
            flash('Competition not found.')
        return render_template('adjudication_system/results.html', competitions=competitions)
