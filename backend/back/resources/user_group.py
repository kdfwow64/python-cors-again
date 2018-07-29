from flask_restful import Resource, reqparse, request
from models.user_group import UserGroupModel
from resources.auth import requires_permission
import json


class UserGroups(Resource):
  @requires_permission('get_user_groups')
  def get(self):
    return {'user_groups': list(map(lambda x: x.json(), UserGroupModel.find_all()))}, 200


class UserGroupRoles(Resource):
  @requires_permission('get_user_group_roles')
  def get(self, id):
    user_group = UserGroupModel.find_by_id(id)
    if user_group:
      return {'roles': list(map(lambda x: x.json(), user_group.roles))}
    return {'error': 'user_group not found'}, 404


class UserGroup(Resource):
  @requires_permission('get_user_group')
  def get(self, id=None):
    queryData = request.args.to_dict()
    if id:
      user_group = UserGroupModel.find_by_id(id)
      if user_group:
        return user_group.json()
      else:
        return {'message': 'user group not found'}, 404
    user_groups = UserGroupModel.find(**queryData)
    return {'user_groups': list(map(lambda x: x.json(), user_groups))}, 200

  @requires_permission('add_user_group')
  def post(self):
    data = json.loads(request.data)

    if 'roles' not in data or len(data['roles']) == 0 or data['roles'] == '':
      return {'error': "The user group roles is empty".format(data['name'])}, 400

    if UserGroupModel.find_by_name(data["name"]):
      return {'message': "A user_group with name '{}' already exists.".format(data["name"])}, 400
    user_group = UserGroupModel(**data)
    # try:
    user_group.save_to_db()
    # except:
    #   return {"message": "An error occurred creating the user_group."}, 500

    return user_group.json(), 201

  @requires_permission('update_user_group')
  def put(self, id):
    data = json.loads(request.data)

    if 'roles' not in data or data['roles'] == '':
      return {'error': "The user group roles is empty".format(data['name'])}, 400

    user_group = UserGroupModel.find_by_id(id)
    if user_group:
      user_group.update(**data)
      return user_group.json(), 201

    return {'error': 'user_group not found'}, 404

  @requires_permission('delete_user_group')
  def delete(self, id):
    user_group = UserGroupModel.find_by_id(id)
    if user_group:
      user_group.delete_from_db()

      return {'success': 'user_group deleted'}, 202

    return {'error': 'user_group not found'}, 404

class Deviceinuser_group(Resource):
  def get(self, name):
    user_group = UserGroupModel.find_by_name(name)
    if user_group:
      return user_group.deviceinuser_group()

class Childinuser_group(Resource):
  def get(self, name):
    user_group = UserGroupModel.find_by_name(name)
    if user_group:
      return user_group.childinuser_group()