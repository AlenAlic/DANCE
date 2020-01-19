from backend.models import db
from backend.errors import bp
from backend.constants import SERVER_ERROR


# noinspection PyUnusedLocal
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return SERVER_ERROR


# noinspection PyUnusedLocal
@bp.app_errorhandler(Exception)
def handle_unexpected_error(error):
    db.session.rollback()
    return SERVER_ERROR
