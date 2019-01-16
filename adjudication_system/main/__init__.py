from flask import Blueprint

bp = Blueprint('main', __name__)

from adjudication_system.main import routes
