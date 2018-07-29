from flask_restful import Resource, request
import json
from resources.auth import requires_permission

from models.user import UserModel


class Users(Resource):
  @requires_permission('get_users')
  def get(self):
    return {'users': list(map(lambda x: x.json(), UserModel.find_all()))}, 200


class User(Resource):
  
  @requires_permission('get_user')
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      user = UserModel.find_by_id(id)
      if user: return user.json()
      else: return {'error': 'user not found'}, 404
    users = UserModel.find(**queryData)
    return {'users': list(map(lambda x: x.json(), users))}, 200

  @requires_permission('delete_user')
  def delete(self, id):
    user = UserModel.find_by_id(id)
    if user:
      user.delete_from_db()
      return {'success': 'user {} deleted'.format(id)}, 202
    return {'error': 'user {} not found'.format(id)},404

  @requires_permission('update_user')
  def put(self, id):
    data = json.loads(request.data)
    if 'user_group' not in data:
      return {'error': "The user group is empty".format(data['username'])}, 400

    user = UserModel.find_by_id(id)
    if user:
      user.update(**data)
      return user.json(), 201

    return {'error': 'user not found'}, 404

  @requires_permission('add_user')
  def post(self):
    data = json.loads(request.data)
    if 'user_group' not in data:
      return {'error': "The user group is empty".format(data['username'])}, 400

    if UserModel.find_by_username(data['username']):
      return {'error': "A user with name '{}' already exists.".format(data['username'])}, 400

    user = UserModel(**data)
    user.hash_password(data['password'])
    try:
      user.save_to_db()
    except:
      return {"error": "An error occurred creating the user."}, 500
    return user.json(), 201