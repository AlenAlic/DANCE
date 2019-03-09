from flask import Blueprint

bp = Blueprint('errors', __name__)

from adjudication_system.errors import handlers
