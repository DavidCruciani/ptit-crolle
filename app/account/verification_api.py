from ..db_class.db import User

def verif_add_user(data_dict):
    if "first_name" not in data_dict or not data_dict["first_name"]:
        return {"message": "Please give a first name for the user"}

    if "last_name" not in data_dict or not data_dict["last_name"]:
        return {"message": "Please give a last name for the user"}

    if "email" not in data_dict or not data_dict["email"]:
        return {"message": "Please give an email for the user"}
    elif User.query.filter_by(email=data_dict["email"]).first():
        return {"message": "Email already exists"}

    if "password" not in data_dict or not data_dict["password"]:
        return {"message": "Please give a password for the user"}
    
    data_dict["role_id"] = 2 # default role is user

    return data_dict

def verif_edit_user(data_dict, user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}
    
    if "first_name" not in data_dict or not data_dict["first_name"]:
        data_dict["first_name"] = user.first_name

    if "last_name" not in data_dict or not data_dict["last_name"]:
        data_dict["last_name"] = user.last_name

    if "email" not in data_dict or not data_dict["email"]:
        data_dict["email"] = user.email
    elif data_dict["email"] != user.email and User.query.filter_by(email=data_dict["email"]).first():
        return {"message": "Email already exists"}

    return data_dict

