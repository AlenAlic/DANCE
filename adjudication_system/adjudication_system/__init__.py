from flask import Blueprint

bp = Blueprint('adjudication_system', __name__)

from adjudication_system.adjudication_system import routes
