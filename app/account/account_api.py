from flask import request
from . import verification_api as VerifApi
from . import account_core as AccountCore

from flask_restx import Namespace, Resource, fields
from ..decorators import api_required
from ..utils.utils import get_user_api


account_ns = Namespace("account", description="Endpoints to manage account actions")

# Define models for request body documentation
# Changed to use JSON body fields, instead of URL parameters
add_user_model = account_ns.model('AddUser', {
    'first_name': fields.String(required=True, description='First name for the user'),
    'last_name': fields.String(required=True, description='Last name for the user'),
    'email': fields.String(required=True, description='Email for the user'),
    'password': fields.String(required=True, description='Password for the user'),
})

edit_user_model = account_ns.model('EditUser', {
    'first_name': fields.String(required=False, description='First name for the user'),
    'last_name': fields.String(required=False, description='Last name for the user'),
    'email': fields.String(required=False, description='Email for the user'),
})


#########
# Users #
#########
    
@account_ns.route('/user/<uid>')
@account_ns.doc(description='Get a users', params={'uid': 'id of a user'})
class GetUsers(Resource):
    method_decorators = [api_required]
    def get(self, uid):
        user = AccountCore.get_user(uid)
        if user:
            return user.to_json(), 200
        return {"message": "User not found"}, 404

@account_ns.route('/add_user')
@account_ns.doc(description='Add new user')
class AddUser(Resource):    
    @account_ns.expect(add_user_model)
    def post(self):
        if request.json:
            verif_dict = VerifApi.verif_add_user(request.json)
            if "message" not in verif_dict:
                user = AccountCore.create_user_core(verif_dict)
                return {"message": f"User created {user.id}", "id": user.id}, 201
            return verif_dict, 400
        return {"message": "Please give data"}, 400

                
@account_ns.route('/edit_user/<id>')
@account_ns.doc(description='Edit user', params={'id': 'id of a user'})
class EditUser(Resource):
    method_decorators = [api_required]
    
    @account_ns.expect(edit_user_model)
    def post(self, id):
        if request.json:            
            user_to_edit = AccountCore.get_user(id)
            if not user_to_edit:
                return {"message": "User not found"}, 404
            
            verif_dict = VerifApi.verif_edit_user(request.json, id)
            if "message" not in verif_dict:
                AccountCore.edit_user_core(verif_dict, id)
                return {"message": "User edited"}, 200
            return verif_dict, 400
        return {"message": "Please give data"}, 400


@account_ns.route('/delete_user/<id>')
@account_ns.doc(description='Delete user', params={'id': 'id of a user'})
class DeleteUser(Resource):
    method_decorators = [api_required]
    def get(self, id):
        api_user = get_user_api(request.headers["X-API-KEY"])
        
        user_to_delete = AccountCore.get_user(id)
        if not user_to_delete:
            return {"message": "User not found"}, 404
        
        if user_to_delete.id == api_user.id:
            return {"message": "You cannot delete your own account"}, 403
        
        if AccountCore.delete_user_core(id):
            return {"message": "User deleted"}, 200
        return {"message": "Error deleting user"}, 400



