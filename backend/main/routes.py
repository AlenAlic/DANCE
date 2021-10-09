from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from backend.main import bp
from backend.main.forms import LoginForm
from backend.models import User
from backend.models.user.util import decode_token
from backend.constants import GET, POST, OK
import os


@bp.route("/", methods=[GET, POST])
@bp.route("/index", methods=[GET, POST])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if request.method == POST:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password", "alert-danger")
                return redirect(url_for("main.index"))
            if user.is_active and user.is_tournament_office_manager():
                login_user(user)
                return redirect(url_for("main.dashboard"))
            else:
                flash("Account inactive", "alert-warning")
                return redirect(url_for("main.index"))
    return render_template("index.html", login_form=form)


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico')


@bp.route("/api/remote_login", methods=[POST])
def login():
    token = decode_token(request.form["token"])
    if token is not None:
        user = User.query.filter(User.user_id == token["id"], User.reset_index == token["reset_index"]).first()
        if user is not None:
            login_user(user)
            return redirect(url_for("admin.index"))
    return redirect(url_for("main.index"))


@bp.route("/dashboard", methods=[GET, POST])
@login_required
def dashboard():
    return render_template("dashboard.html")


@bp.route("/logout", methods=[GET])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route('/ping', methods=[GET])
def ping():
    return OK
