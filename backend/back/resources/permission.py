from flask_restful import Resource, reqparse, request
from models.permission import PermissionModel
import json


class Permissions(Resource):
  def get(self):
    return {'permissions': list(map(lambda x: x.json(), PermissionModel.find_all()))}, 200

class Permission(Resource):
    
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      permission = PermissionModel.find_by_id(id)
      if permission: return permission.json()
      else: return {'error': 'user_group not found'}, 404
    permissions = PermissionModel.find(**queryData)
    return {'permissions': list(map(lambda x: x.json(), permissions))}, 200

  def post(self):
    data = json.loads(request.data)
    if PermissionModel.find_by_name(data["name"]):
      return {'error': "A permission with name '{}' already exists.".format(data["name"])}, 400
    permission = PermissionModel(**data)
    try:
      permission.save_to_db()
    except:
      return {"error": "An error occurred creating the permission."}, 500
    return permission.json(), 201

  def put(self, id):
    data = json.loads(request.data)
    permission = PermissionModel.find_by_id(id)

    if permission:
      permission.update(**data)
      return permission.json()

    return {'error': 'permission not found'}, 404

  def delete(self, name):
    permission = PermissionModel.find_by_name(name)
    if permission:
      permission.delete_from_db()
      return {'success': 'permission deleted'}, 202
    return {'error': 'permission not found'}, 404