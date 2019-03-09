from flask import render_template
from adjudication_system import db
from adjudication_system.errors import bp
import traceback


# noinspection PyUnusedLocal
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html')


# noinspection PyUnusedLocal
@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html')


# noinspection PyUnusedLocal
@bp.app_errorhandler(Exception)
def handle_unexpected_error(error):
    db.session.rollback()
    e = traceback.format_exc()
    return render_template('errors/500.html', error=e)
