from flask_restful import Resource, reqparse, request
from models.group import GroupModel
import json

class Group(Resource):
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:
      group = GroupModelModel.find_by_name(name)
      if location:
        return group.json(), 200
      else:
        return {'error': 'group not found'}, 404
    groups = GroupModel.find(**queryData)
    return {'groups': list(map(lambda x: x.json(), groups))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    if GroupModel.find_by_name(name):
      return {'error': "A group with name '{}' already exists.".format(name)}, 400
    group = GroupModel(**data)
    try:
      group.save_to_db()
    except:
      return {"error": "An error occurred creating the group."}, 500
    return group.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    group = GroupModel.find_by_name(name)
    if group:
      group.update(**data)
    else:
      return {'error': 'Group not found'}, 404
    return group.json(), 201

  def delete(self, name):
    group = GroupModel.find_by_name(name)
    if group:
      group.delete_from_db()
    else:
      return {'error': 'Group not found'}, 404
    return {'success': 'group deleted'}, 202

class GroupList(Resource):
  def get(self):
    return {'groups': list(map(lambda x: x.json(), GroupModel.query.all()))}, 200

class Deviceingroup(Resource):
  def get(self, name):
    group = GroupModel.find_by_name(name)
    if group:
      return group.deviceingroup()

class Childingroup(Resource):
  def get(self, name):
    group = GroupModel.find_by_name(name)
    if group:
      return group.childingroup()