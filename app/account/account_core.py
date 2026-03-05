from app.utils.utils import generate_api_key

from .. import db
from ..db_class.db import User, Role

def get_all_roles():
    """Return all roles"""
    return Role.query.all()

def get_user(id):
    """Return the user"""
    return User.query.get(id)


def edit_user_core(form_dict, id) -> tuple[User, str]:
    """Edit the user to the DB"""
    try:
        user = get_user(id)

        user.first_name=form_dict["first_name"]
        user.last_name=form_dict["last_name"]
        user.email=form_dict["email"]
        if form_dict.get("password"):  
            user.password = form_dict["password"] 

        db.session.commit()
        return user, "User updated successfully"
    except Exception as e:
        return None, f"Error updating user"


def create_user_core(form_dict):
    """Create the user to the DB"""
    try:
        # Check if the user already exists
        if User.query.filter_by(email=form_dict["email"]).first():
            return None, "User already exists"
        user = User(
            first_name=form_dict["first_name"],
            last_name=form_dict["last_name"],
            email=form_dict["email"],
            password=form_dict["password"],
            role_id=form_dict["role_id"],
            api_key = generate_api_key()
        )
        db.session.add(user)
        db.session.commit()
        return user, "Registration successfully, you can now login"
    except Exception as e:
        return None, f"Error during registration"