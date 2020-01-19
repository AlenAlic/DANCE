from flask_restplus import Namespace, Resource, abort
from backend.models import db
from backend.models.dance import Dance
from backend.models.discipline import Discipline
from backend.models.dancing_class import DancingClass
from backend.constants import AL_TOURNAMENT_OFFICE_MANAGER
from backend.models.user.wrappers import login_required, requires_access_level


api = Namespace("dependencies", description="Dependencies")


def dependencies(dances=True, disciplines=True, classes=True):
    data = {}
    if dances:
        data.update({"dances": [d.json() for d in Dance.query.order_by(Dance.order).all()]})
    if disciplines:
        data.update({"disciplines": [d.json() for d in Discipline.query.order_by(Discipline.name).all()]})
    if classes:
        data.update({"classes": [d.json() for d in DancingClass.query.order_by(DancingClass.name).all()]})
    return data


@api.route("/")
class Dependencies(Resource):

    @api.doc("dependencies")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """All competition dependencies"""
        return dependencies()


@api.route("/dance")
class DependenciesAPIDance(Resource):

    @api.doc("get_dance")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """Get all dances"""
        return dependencies(disciplines=False, classes=False)

    @api.doc("post_dance")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @api.param("discipline_id", "Discipline_id")
    @api.param("order", "Order")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new dance"""
        dance = Dance()
        dance.name = api.payload["name"]
        dance.tag = api.payload["tag"]
        dance.discipline_id = api.payload["discipline_id"]
        dance.order = api.payload["order"]
        db.session.add(dance)
        db.session.commit()
        return dependencies(classes=False)


@api.route("/dance/<int:dance_id>")
class DependenciesAPISpecificDance(Resource):

    @api.doc("patch_dance")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @api.param("discipline_id", "Discipline_id")
    @api.param("order", "Order")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, dance_id):
        """Update dance"""
        dance = Dance.query.get(dance_id)
        if dance is not None:
            dance.name = api.payload["name"]
            dance.tag = api.payload["tag"]
            dance.discipline_id = api.payload["discipline_id"]
            dance.order = api.payload["order"]
            db.session.commit()
            return dependencies(classes=False)
        abort(404, "Unknown dance_id")

    @api.doc("delete_dance")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, dance_id):
        """Delete dance"""
        dance = Dance.query.get(dance_id)
        if dance is not None:
            db.session.delete(dance)
            db.session.commit()
            return dependencies(classes=False)
        abort(404, "Unknown dance_id")


@api.route("/discipline")
class DependenciesAPIDiscipline(Resource):

    @api.doc("get_discipline")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """Get all discipline"""
        return dependencies(dances=False, classes=False)

    @api.doc("post_discipline")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @api.param("dances", "List of dance_ids")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new discipline"""
        discipline = Discipline()
        discipline.name = api.payload["name"]
        discipline.tag = api.payload["tag"]
        discipline.dances = Dance.query.filter(Dance.dance_id.in_(api.payload["dances"])).all()
        db.session.add(discipline)
        db.session.commit()
        return dependencies(classes=False)


@api.route("/discipline/<int:discipline_id>")
class DependenciesAPISpecificDiscipline(Resource):

    @api.doc("patch_discipline")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @api.param("dances", "List of dance_ids")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, discipline_id):
        """Update discipline"""
        discipline = Discipline.query.get(discipline_id)
        if discipline is not None:
            discipline.name = api.payload["name"]
            discipline.tag = api.payload["tag"]
            discipline.dances = Dance.query.filter(Dance.dance_id.in_(api.payload["dances"])).all()
            db.session.commit()
            return dependencies(classes=False)
        abort(404, "Unknown discipline_id")

    @api.doc("delete_discipline")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, discipline_id):
        """Delete discipline"""
        discipline = Discipline.query.get(discipline_id)
        if discipline is not None:
            db.session.delete(discipline)
            db.session.commit()
            return dependencies(classes=False)
        abort(404, "Unknown discipline_id")


@api.route("/class")
class DependenciesAPIDancingClass(Resource):

    @api.doc("get_class")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def get(self):
        """Get all classes"""
        return dependencies(dances=False, disciplines=False)

    @api.doc("post_class")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def post(self):
        """Create new class"""
        dancing_class = DancingClass()
        dancing_class.name = api.payload["name"]
        dancing_class.tag = api.payload["tag"]
        db.session.add(dancing_class)
        db.session.commit()
        return dependencies(dances=False, disciplines=False)


@api.route("/class/<int:dancing_class_id>")
class DependenciesAPISpecificDancingClass(Resource):

    @api.doc("patch_class")
    @api.param("name", "Name")
    @api.param("tag", "Tag")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def patch(self, dancing_class_id):
        """Update class"""
        dancing_class = DancingClass.query.get(dancing_class_id)
        if dancing_class is not None:
            dancing_class.name = api.payload["name"]
            dancing_class.tag = api.payload["tag"]
            db.session.commit()
            return dependencies(dances=False, disciplines=False)
        abort(404, "Unknown dancing_class_id")

    @api.doc("delete_class")
    @login_required
    @requires_access_level([AL_TOURNAMENT_OFFICE_MANAGER])
    def delete(self, dancing_class_id):
        """Delete class"""
        dancing_class = DancingClass.query.get(dancing_class_id)
        if dancing_class is not None:
            db.session.delete(dancing_class)
            db.session.commit()
            return dependencies(dances=False, disciplines=False)
        abort(404, "Unknown dancing_class_id")
