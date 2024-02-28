import os
import uuid
import random
import string
from ..db_class.db import User

def isUUID(uid):
    try:
        uuid.UUID(str(uid))
        return True
    except ValueError:
        return False

def generate_api_key(length=60):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_user_api(api_key):
    return User.query.filter_by(api_key=api_key).first()

def verif_api_key(headers):
    if not "X-API-KEY" in headers:
        return {"message": "Error no API key pass"}, 403
    user = get_user_api(headers["X-API-KEY"])
    if not user:
        return {"message": "API key not found"}, 403
    return {}

def form_to_dict(form):
    loc_dict = dict()
    for field in form._fields:
        if field == "files_upload":
            loc_dict[field] = dict()
            loc_dict[field]["data"] = form._fields[field].data
            loc_dict[field]["name"] = form._fields[field].name
        elif not field == "submit" and not field == "csrf_token":
            loc_dict[field] = form._fields[field].data
    return loc_dict


def create_specific_dir(specific_dir):
    if not os.path.isdir(specific_dir):
        os.mkdir(specific_dir)

