from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.role_permission import RolePermissionModel
import json

class RolePermission(Resource):
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      role_permission = RolePermissionModel.findById(id)
      if role_permission: return role_permission.json()
      else: return {'error': 'role_permission not found'}, 404
    role_permissions = RolePermissionModel.find(**queryData)
    return {'role_permissions': list(map(lambda x: x.json(), role_permissions))}, 200

    def post(self, name):
        data = json.loads(request.data)
        if RolePermissionModel.find_by_name(name):
          return {'error': "A role permission with name '{}' already exists.".format(name)}, 400
        role_permission = RolePermissionModel(**data)
        try:
          role_permission.save_to_db()
        except:
          return {"error": "An error occurred creating the role permission."}, 500
        
        return role_permission.json(), 201 
    
    def put(self, name):
        data = json.loads(request.data)
        role_permission = RolePermissionModel.find_by_name(name)
    
        if role_permission:
          role_permission = RolePermissionModel(**data)
          
        else:
          role_permission = RolePermissionModel(**data)
        
        role_permission.save_to_db(commit=True)
    
        return role_permission.json(), 201
    
  def delete(self, name):
    role_permission = RolePermissionModel.find_by_name(name)
    if role_permission:
      role_permission.delete_from_db()
    return {'success': 'role permission deleted'}, 202