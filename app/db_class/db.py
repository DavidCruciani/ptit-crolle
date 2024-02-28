from .. import db, login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import  UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, index=True)
    password_hash = db.Column(db.String(128))
    api_key = db.Column(db.String(60), index=True)
    
    def is_admin(self):
        r = Role.query.get(self.role_id)
        if r.admin:
            return True
        return False

    def read_only(self):
        r = Role.query.get(self.role_id)
        if r.read_only:
            return True
        return False

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            "id": self.id, 
            "first_name": self.first_name, 
            "last_name": self.last_name, 
            "email": self.email, 
            "org_id": self.org_id, 
            "role_id": self.role_id
        }

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

    def read_only(self):
        return True
    
login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    read_only = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id, 
            "name": self.name,
            "description": self.description,
            "admin": self.admin,
            "read_only": self.read_only
        }