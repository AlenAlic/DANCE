from flask import redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import PasswordField


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("flask_app.index"))
        else:
            return self.render(self._template)


class AdjudicatorSystemView(ModelView):
    column_hide_backrefs = False
    page_size = 500

    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))


class UserView(AdjudicatorSystemView):
    column_exclude_list = ["password_hash", ]
    form_excluded_columns = ["password_hash", ]
    form_extra_fields = {"password2": PasswordField("Password")}

    # noinspection PyPep8Naming
    def on_model_change(self, form, User, is_created):
        if form.password2.data != "":
            User.set_password(form.password2.data)
