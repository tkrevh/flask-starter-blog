from .. import app, db, api
from flask.ext import security
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask.ext.security.signals import user_registered
from forms import ExtendedRegisterForm
import pytz

# Define models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, security.RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, security.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))

    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = relationship("Post", backref="author")
    comments = relationship("Comment", backref="author")
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(32))
    current_login_ip = db.Column(db.String(32))
    login_count = db.Column(db.Integer())
    timezone = db.Column(db.String(64))

    def get_tz(self):
        if self.timezone:
            return pytz.timezone(self.timezone)
        else:
            return app.config.get("DEFAULT_TIMEZONE", pytz.utc)

    def dict(self):
        """
        A dictionary representation that can be used for JSON serialization
        """
        return {
            "email": self.email,
            "active": self.active,
            "confirmed_at": api.serialize_date(self.confirmed_at),
            "timezone": self.timezone
        }

    def __str__(self):
        return self.name or self.email

    def can_post(self):
        return self.has_role('admin') or self.has_role('editor')
        
    def can_comment(self):
        return self.has_role('admin') or self.has_role('commentator') or self.has_role('editor')
        
# Setup Flask-Security
user_datastore = security.SQLAlchemyUserDatastore(db, User, Role)
app.security = security.Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm, register_form=ExtendedRegisterForm)

# Custom signal handlers
@user_registered.connect_via(app)
def user_registered_sighandler(app, user, confirm_token):
    default_role = user_datastore.find_role("commentator")
    user_datastore.add_role_to_user(user, default_role)
    db.session.commit()
