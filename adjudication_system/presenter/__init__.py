from flask import Blueprint

bp = Blueprint('presenter', __name__)

from adjudication_system.presenter import routes
