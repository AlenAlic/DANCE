from flask import Flask, request
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_admin import Admin
from backend.admin import MyAdminIndexView, AdjudicatorSystemView, UserView
from backend.models.user import Anonymous
from config import Config
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER, AL_FLOOR_MANAGER, AL_PRESENTER
from datetime import datetime


migrate = Migrate()
login = LoginManager()
admin = Admin(template_mode="bootstrap3", index_view=MyAdminIndexView())


def create_app(config_class=Config):
    from backend.models import User, Event, Competition, DancingClass, Discipline, Dance, Round, \
        Heat, Couple, Adjudicator, Mark, CouplePresent, RoundResult, FinalPlacing, DanceActive, CompetitionMode, \
        Dancer, AdjudicatorCompetitionAssignment, EventResult

    # Create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False

    from .models import db, login
    # Init add-ons
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"))
    login.init_app(app)
    login.login_view = 'main.index'
    login.anonymous_user = Anonymous
    admin.init_app(app)
    admin.add_view(UserView(User, db.session))
    admin.add_view(AdjudicatorSystemView(Event, db.session))
    admin.add_view(AdjudicatorSystemView(EventResult, db.session))
    admin.add_view(AdjudicatorSystemView(Competition, db.session))
    admin.add_view(AdjudicatorSystemView(DancingClass, db.session))
    admin.add_view(AdjudicatorSystemView(Discipline, db.session))
    admin.add_view(AdjudicatorSystemView(Dance, db.session))
    admin.add_view(AdjudicatorSystemView(Adjudicator, db.session))
    admin.add_view(AdjudicatorSystemView(AdjudicatorCompetitionAssignment, db.session))
    admin.add_view(AdjudicatorSystemView(Dancer, db.session))
    admin.add_view(AdjudicatorSystemView(Couple, db.session))
    admin.add_view(AdjudicatorSystemView(Round, db.session))
    admin.add_view(AdjudicatorSystemView(DanceActive, db.session))
    admin.add_view(AdjudicatorSystemView(Heat, db.session))
    admin.add_view(AdjudicatorSystemView(Mark, db.session))
    admin.add_view(AdjudicatorSystemView(FinalPlacing, db.session))
    admin.add_view(AdjudicatorSystemView(CouplePresent, db.session))
    admin.add_view(AdjudicatorSystemView(RoundResult, db.session))

    # Shell command for creating tournament office (admin) account, a floor manager account, and a presenter account
    def create_tournament_office(tournament_office_password, floor_manager_password, presenter_password):
        with app.app_context():
            user = User()
            user.username = "admin"
            user.set_password(tournament_office_password)
            user.is_active = True
            user.access = AL_TOURNAMENT_OFFICE_MANAGER
            db.session.add(user)
            fm = User()
            fm.username = "floor"
            fm.set_password(floor_manager_password)
            fm.is_active = True
            fm.access = AL_FLOOR_MANAGER
            db.session.add(fm)
            p = User()
            p.username = "presenter"
            p.set_password(presenter_password)
            p.is_active = True
            p.access = AL_PRESENTER
            db.session.add(p)
            db.session.commit()

    # Shell command for changing a password
    def change_password(username, password):
        with app.app_context():
            user = User.query.filter(User.username == username)
            if user is not None:
                user.set_password(password)
                db.session.commit()
            else:
                print(f"Could not find user with username: '{username}'")

    @app.shell_context_processor
    def make_shell_context():
        return {"create_tournament_office": create_tournament_office, "change_password": change_password}

    @app.before_request
    def before_request_callback():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin and origin in config_class.ALLOWED_URLS:
            response.headers["Access-Control-Allow-Origin"] = origin
        if request.method == "OPTIONS":
            response.headers["Access-Control-Allow-Methods"] = "DELETE, GET, POST, PUT, PATCH"
            headers = request.headers.get("Access-Control-Request-Headers")
            if headers:
                response.headers["Access-Control-Allow-Headers"] = headers
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    # Register api
    from backend.main import bp as main_bp
    app.register_blueprint(main_bp)

    from backend.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from backend import apis
    apis.init_app(app)

    return app
