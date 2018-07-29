from flask_restful import Resource, reqparse, request
from models.check_result import CheckResultModel
import json

class CheckResult(Resource):
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:
      check_result = CheckResultModel.find_by_name(name)
      if check_result:
        return check_result.json(), 200
      else:
        return {'error': 'check_result not found'}, 404
    check_results = CheckResultModel.find(**queryData)
    return {'check_results': list(map(lambda x: x.json(), check_results))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    if CheckResultModel.find_by_name(name):
      return {'error': "A check_result with name '{}' already exists.".format(name)}, 400
    check_result = CheckResultModel(**data)
    try:
      check_result.save_to_db()
    except:
      return {"error": "An error occurred creating the check_result."}, 500
    return check_result.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    check_result = CheckResultModel.find_by_name(name)
    if check_result:
      check_result.update(**data)
    else:
      return {'error': 'check_result not found'}, 404
    check_result.save_to_db(commit=True)
    return check_result.json(), 201

  def delete(self, name):
    check_result = CheckResultModel.find_by_name(name)
    if check_result:
      check_result.delete_from_db()
    else:
      return {'error': 'check_result not found'}, 404
    return {'success': 'check_result deleted'}, 202
