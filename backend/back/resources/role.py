from flask_restful import Resource, reqparse, request
from models.role import RoleModel
from resources.auth import requires_permission
import json


class Roles(Resource):
  @requires_permission('get_roles')
  def get(self):
    return {'roles': list(map(lambda x: x.json(), RoleModel.find_all()))}


class RolePermissions(Resource):
  @requires_permission('get_role_permissions')
  def get(self, id):
    role = RoleModel.find_by_id(id)
    if role:
      return {'permissions': list(map(lambda x: x.json(), role.permissions))}, 200
    return {'error': 'role not found'}, 404


class Role(Resource):
  @requires_permission('get_role')
  def get(self, id=None):
    queryData = request.args.to_dict()
    if id:
      role = RoleModel.find_by_id(id)
      if role:
        return role.json()
      else:
        return {'error': 'role not found'}, 404
    roles = RoleModel.find(**queryData)
    return {'roles': list(map(lambda x: x.json(), roles))}, 200

  @requires_permission('add_role')
  def post(self):
    data = json.loads(request.data)

    if 'permissions' not in data or len(data['permissions']) == 0 or data['permissions'] == '':
      return {'error': "The role permissions is empty".format(data['name'])}, 400

    if RoleModel.find_by_name(data["name"]):
      return {'error': "A role with name '{}' already exists.".format(data["name"])}, 400
    role = RoleModel(**data)
    try:
      role.save_to_db()
    except:
      return {"error": "An error occurred creating the role."}, 500

    return role.json(), 201

  @requires_permission('update_role')
  def put(self, id):
    data = json.loads(request.data)

    if 'permissions' not in data or data['permissions'] == '':
      return {'error': "The role permissions is empty".format(data['name'])}, 400

    role = RoleModel.find_by_id(id)

    if role:
      role.update(**data)
      return role.json(), 201

    return {'error': 'role not found'}, 404

  @requires_permission('delete_role')
  def delete(self, id):
    role = RoleModel.find_by_id(id)
    if role:
      role.delete_from_db()
      return {'success': 'role deleted'}, 202

    return {'error': 'role not found'}, 404

