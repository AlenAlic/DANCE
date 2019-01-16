from flask import jsonify, request
from flask_login import login_required
from adjudication_system import db
from adjudication_system.models import CouplePresent
from adjudication_system.api import bp


@bp.route('/present/<int:present_id>/present', methods=["GET", "PATCH"])
@login_required
def present_present(present_id):
    present = CouplePresent.query.get_or_404(present_id)
    if request.method == "PATCH":
        present.present = not present.present
        db.session.commit()
    return jsonify(present.present)
