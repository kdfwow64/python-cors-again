from flask_restful import Resource, reqparse, request
from models.check import CheckModel
import json

class Check(Resource):
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:
      check = CheckModel.find_by_name(name)
      if check:
        return check.json(), 200
      else:
        return {'error': 'check not found'}, 404
    checks = CheckModel.find(**queryData)
    return {'checks': list(map(lambda x: x.json(), checks))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    check = CheckModel(**data)
    try:
      check.save_to_db()
    except:
      return {"error": "An error occurred creating the check."}, 500
    return check.json(), 201

  def put(self, id):
    data = json.loads(request.data)
    check = CheckModel.find_by_id(id)
    if check:
      check.update(**data)
    else:
      return {'error': 'check not found'}, 404
    check.save_to_db(commit=True)
    return check.json(), 201

  def delete(self, name):
    check = CheckModel.find_by_name(name)
    if check:
      check.delete_from_db()
    else:
      return {'error': 'check not found'}, 404
    return {'success': 'check deleted'}, 202
