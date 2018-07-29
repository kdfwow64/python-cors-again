from flask_restful import Resource, reqparse, request
from models.eval import EvalModel
import json

class Eval(Resource):
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      eval = EvalModel.find_by_id(id)
      if eval: return eval.json(), 200
      else: return {'error': 'evaluation not found'}, 404
    eval = EvalModel.find(**queryData)
    return {'evals': list(map(lambda x: x.json(), eval))}, 200

  def post(self, **somedata):
    data = json.loads(request.data)
    data["status"] = "NEW"
    eval = EvalModel(**data)
    try:
      eval.save_to_db()
    except:
      return {"error": "An error occurred creating the eval."}, 500
    return eval.json(), 201

  def put(self, id):
    data = json.loads(request.data)
    eval = EvalModel.find_by_id(id)
    if eval:
      eval.update(**data)
    else:
      return {'error': 'evaluation not found'}, 404
    return eval.json(), 201

  def delete(self, id):
    eval = EvalModel.find_by_id(id)
    if eval:
      eval.delete_from_db()
    else:
      return {'error': 'evaluation not found'}, 404
    return {'success': 'evaluation deleted'}, 202
