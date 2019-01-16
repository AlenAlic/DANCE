from flask import Blueprint

bp = Blueprint('as_api', __name__)

from adjudication_system.api import adjudication
from adjudication_system.api import tournament_office
from adjudication_system.api import floor_manager
