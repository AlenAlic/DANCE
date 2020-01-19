from flask import Blueprint
from flask_restplus import Api
from .auth import api as auth
from .config import api as config
from .user import api as user
from .event import api as event
from .competition import api as competition
from .dependencies import api as dependencies
from .adjudicators import api as adjudicators
from .couples import api as couples
from .dancers import api as dancers
from .round import api as r
from .adjudication import api as adjudication
from .floor_manager import api as floor_manager


authorizations = {
    "bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}


bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp, doc="/doc", authorizations=authorizations, security="bearer", title="DANCE API", version="1.0")
    

api.add_namespace(adjudicators)
api.add_namespace(adjudication)
api.add_namespace(auth)
api.add_namespace(competition)
api.add_namespace(couples)
api.add_namespace(config)
api.add_namespace(dancers)
api.add_namespace(dependencies)
api.add_namespace(event)
api.add_namespace(floor_manager)
api.add_namespace(r)
api.add_namespace(user)


def init_app(app):
    from .debug import api as debug
    if app.config.get("DEBUG"):
        api.add_namespace(debug)

    app.register_blueprint(bp)
