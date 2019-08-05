from flask import render_template
from flask_login import login_required
from adjudication_system.presenter import bp
from adjudication_system.models import requires_access_level
from adjudication_system.values import *


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
@requires_access_level([ACCESS[PRESENTER]])
def dashboard():
    return render_template('presenter/dashboard.html')
