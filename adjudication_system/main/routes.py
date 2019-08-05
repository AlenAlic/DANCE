from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from adjudication_system.main import bp
from adjudication_system.main.forms import LoginForm
from adjudication_system.models import User


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'alert-danger')
            return redirect(url_for('main.index'))
        if user.is_active:
            login_user(user)
            return redirect(url_for('main.dashboard'))
    return render_template('index.html', title='Home', login_form=form)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if current_user.is_adjudicator():
        return redirect(url_for('adjudication_system.adjudicator_dashboard'))
    if current_user.is_floor_manager():
        return redirect(url_for('adjudication_system.floor_manager_start_page'))
    if current_user.is_presenter():
        return redirect(url_for('presenter.dashboard'))
    return render_template('dashboard.html')


@bp.route('/sw.js', methods=['GET'])
def sw():
    return current_app.send_static_file('sw.js')


@bp.route('/offline', methods=['GET'])
def offline():
    return render_template('offline.html')


@bp.route('/switch_page', methods=['GET'])
@login_required
def switch_page():
    users = User.query.filter(User.adjudicator_id.isnot(None)).all()
    return render_template('switch_page.html', users=users)


@bp.route('/switch', methods=['GET'])
@login_required
def switch():
    user_id = request.args.get('user_id', 1, type=int)
    user = User.query.get(user_id)
    logout_user()
    login_user(user)
    return redirect(url_for('main.dashboard'))
